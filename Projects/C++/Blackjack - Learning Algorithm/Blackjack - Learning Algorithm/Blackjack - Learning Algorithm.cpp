#include <iostream>     // std::cout                                               
#include <algorithm>    // std::shuffle
#include <array>        // std::array
#include <random>       // std::default_random_engine
#include <chrono> 
#include <deque>
#include <list>
#include <numeric>
#include <functional>
#include <iomanip>
#include <conio.h>

using namespace std;

#define RED(x) "\033[1;31m" << x << "\033[0m"
#define BLUE(x) "\033[1;34m" << x << "\033[0m"
#define GREEN(x) "\033[1;32m" << x << "\033[0m"
#define BROWN(x) "\033[1;33m" << x << "\033[0m"
#define ROUND(x, r) fixed << setprecision(r) << x
#define Pc(p, q, Kp, Kq) "P[" << p << "]" << "[" << q << "]" << "[" << Kp << "]" << "[" << Kq << "]"
#define Nc(p, q, Kp, Kq) "N[" << p << "]" << "[" << q << "]" << "[" << Kp << "]" << "[" << Kq << "]"

typedef unsigned number;

enum card {
    two = 2, three, four,
    five, six, seven,
    eight, nine, ten,
    jack = 2, queen = 3,
    king = 4, ace = 11
};

void print(const list<number> args) {
    for (const number& item : args)
        cout << item << "\t";
    cout << endl;
}

void Shuffle_Deck(deque<card>& deck) {
    number seed = chrono::system_clock::now().time_since_epoch().count();
    shuffle(deck.begin(), deck.end(), default_random_engine(seed));
}

deque<card> New_deck() {
    return deque<card> {
        two, two, two, two,
            three, three, three, three,
            four, four, four, four,
            five, five, five, five,
            six, six, six, six,
            seven, seven, seven, seven,
            eight, eight, eight, eight,
            nine, nine, nine, nine,
            ten, ten, ten, ten,
            jack, jack, jack, jack,
            queen, queen, queen, queen,
            king, king, king, king,
            ace, ace, ace, ace};
}

card Draw(deque<card>& deck) {
    card c = deck.front();
    deck.pop_front();
    return c;
}

number Suma_oczek(deque<card>& reka) {
    number s = 0;
    for (card& x : reka) s += x;
    return s;
}

bool Czy_przegral(deque<card>& reka) {
    if (Suma_oczek(reka) == 22 && reka.size() == 2)
        return false;
    else if (Suma_oczek(reka) > 21)
        return true;
    else
        return false;
}

bool Koniec_partii(deque<card>& gracz1, deque<card>& gracz2, bool gracz1_stop, bool gracz2_stop) {
    if (gracz1_stop == 1 && gracz2_stop == 1)
        return true;
    else if (Czy_przegral(gracz1) || Czy_przegral(gracz2))
        return true;
    else
        return false;
}

void Fill(float* tensor, const list<number> shape, number value = 0) {
    number size = accumulate(shape.begin(), shape.end(), 1, multiplies<number>());
    fill((number*)tensor, (number*)tensor + size, value);
}

void print_reka(deque<card> reka) {
    for (card& x : reka) {
        cout << x << "\t";
    }
}

float P[23][23][10][10];
float N[23][23][10][10];

deque<card> gracz_AI;
deque<card> gracz;
char znak;
number tempP{ 0 };

int main() {

    bool stop_AI = false;
    bool stop_pl = false;
    bool diagnostyka = false;
    number n{ 0 };
    cout << BROWN("Program learns to play Blackjack") << endl << endl;

    cout << BROWN("Legend: ") << endl;
    cout << "p - value of player's p hand" << endl;
    cout << "q - value of player's q hand" << endl;
    cout << "Kp - number of cards on player's p hand" << endl;
    cout << "Kq - number of cards on player's q hand" << endl;
    cout << "P[p][q][Kp][Kq] - probability of failure after drawing a card for a given state of the game, updated based on the results of simulation games and further games" << endl;
    cout << "N[p][q][Kp][Kq] - number of occurences for a given state of the game" << endl << endl;


    cout << "Specify number of simulations, on which algorithm will learn n -> ";
    cin >> n;

    cout << "Do you want to print P and N each time it gets updated?  T - yes\n";
    znak = _getch();

    diagnostyka = (znak == 'T' || znak == 't') ? 1 : 0;

    cout << "\nSimulating...\n";

    Fill((float*)P, { 23, 23, 10, 10 }, 0);
    Fill((float*)N, { 23, 23, 10, 10 }, 1);

    while (n--) {

        stop_AI = false;
        gracz_AI.clear();
        gracz.clear();
        deque<card> deck = New_deck();
        Shuffle_Deck(deck);

        do {
            number
                sum_ai = Suma_oczek(gracz_AI),
                sum_pl = Suma_oczek(gracz),
                hand_ai = gracz_AI.size(),
                hand_pl = gracz.size();

            // pointers to the value before drawing a card
            float* probability = &P[sum_pl][sum_ai][hand_pl][hand_ai];
            float* counts = &N[sum_pl][sum_ai][hand_pl][hand_ai];


            gracz.push_front(Draw(deck));
            *counts += 1;
            *probability += (Czy_przegral(gracz) - *probability) / *counts;   //update of average w/l ratio

            if (diagnostyka) {
                cout << RED(ROUND(*probability, 2)) << "\t";
                cout << BLUE(ROUND(*counts, 0)) << "\t";
                print({ sum_ai, sum_pl, hand_ai, hand_pl });
            }

            if (Czy_przegral(gracz)) break;


            sum_ai = Suma_oczek(gracz_AI);
            sum_pl = Suma_oczek(gracz);
            hand_ai = gracz_AI.size();
            hand_pl = gracz.size();

            // pointers to the value before drawing a card
            probability = &P[sum_ai][sum_pl][hand_ai][hand_pl];
            counts = &N[sum_ai][sum_pl][hand_ai][hand_pl];

            if (!stop_AI) {
                if (*probability <= 0.5) {
                    gracz_AI.push_front(Draw(deck));
                    *counts += 1;
                    *probability += (Czy_przegral(gracz_AI) - *probability) / *counts;
                }
                else
                    stop_AI = true;

                // diagnostics
                if (diagnostyka) {
                    cout << RED(ROUND(*probability, 2)) << "\t";
                    cout << BLUE(ROUND(*counts, 0)) << "\t";
                    print({ sum_ai, sum_pl, hand_ai, hand_pl });
                }
            }


        } while (!Koniec_partii(gracz_AI, gracz, stop_AI, 0));
    }


    cout << "\nSimulated successfully!" << endl << endl;

    do {
        deque<card> deck = New_deck();
        number p, q, Kp, Kq{ 0 };


        cout << BROWN("\nMenu: ") << endl;
        cout << "1. Print given P[p][q][Kp][Kq] and N[p][q][Kp][Kq]" << endl;
        cout << "2. Play a game of Blackjack with an AI" << endl;
        cout << "3. Close program" << endl;

        do {
            znak = _getch();
        } while (znak != '1' && znak != '2' && znak != '3');

        switch (znak) {
        case '1':
            cout << "\np -> "; cin >> p;
            cout << "q -> "; cin >> q;
            cout << "Kp -> "; cin >> Kp;
            cout << "Kq -> "; cin >> Kq;

            cout << endl << Pc(p, q, Kp, Kq) << " = " << RED(ROUND(P[p][q][Kp][Kq], 2));
            cout << endl << Nc(p, q, Kp, Kq) << " = " << BLUE(ROUND(N[p][q][Kp][Kq], 0)) << endl;
            break;
        case '2':
            stop_pl = false;
            stop_AI = false;
            gracz_AI.clear();
            gracz.clear();
            Shuffle_Deck(deck);
            do {
                number
                    sum_ai = Suma_oczek(gracz_AI),
                    sum_pl = Suma_oczek(gracz),
                    hand_ai = gracz_AI.size(),
                    hand_pl = gracz.size();

                // pointers to the value before drawing a card
                float* probability = &P[sum_pl][sum_ai][hand_pl][hand_ai];
                float* counts = &N[sum_pl][sum_ai][hand_pl][hand_ai];

                if (!stop_pl) {
                    cout << BROWN("\n\nYour hand:\t"); print_reka(gracz);
                    cout << BROWN("\nYour total card value: "); cout << Suma_oczek(gracz);
                    cout << "\nEnemy AI has " << Suma_oczek(gracz_AI) << " total value in " << gracz_AI.size() << " cards" << endl << endl;
                    cout << "\nD - Draw a card | Z - Pass";
                    znak = NULL;
                    while (znak != 'D' && znak != 'd' && znak != 'Z' && znak != 'z') znak = _getch();
                    if (znak == 'D' || znak == 'd') {
                        gracz.push_front(Draw(deck));
                    }
                    else stop_pl = true;
                }

                *counts += 1;
                *probability += (Czy_przegral(gracz) - *probability) / *counts;

                // diagnostics
                cout << endl << endl << RED(ROUND(*probability, 2)) << "\t";
                cout << BLUE(ROUND(*counts, 0)) << "\t";
                print({ sum_pl, sum_ai, hand_pl, hand_ai });

                if (Czy_przegral(gracz)) {
                    cout << RED("\nYou lose!") << endl;
                    cout << "\nYour total card value: " << Suma_oczek(gracz) << endl;
                    cout << "Total value of AI's hand: " << Suma_oczek(gracz_AI) << endl;
                    break;
                }

                sum_ai = Suma_oczek(gracz_AI);
                sum_pl = Suma_oczek(gracz);
                hand_ai = gracz_AI.size();
                hand_pl = gracz.size();

                // pointers to the value before drawing a card
                probability = &P[sum_ai][sum_pl][hand_ai][hand_pl];
                counts = &N[sum_ai][sum_pl][hand_ai][hand_pl];

                if (stop_AI == false) {
                    if (*probability <= 0.5) {
                        gracz_AI.push_front(Draw(deck));
                        cout << "\nAI drew a card";
                        *counts += 1;
                        *probability += (Czy_przegral(gracz_AI) - *probability) / *counts;
                    }
                    else
                    {
                        cout << "\nAI passed";
                        stop_AI = true;
                    }
                }

                cout << endl << endl << RED(ROUND(*probability, 2)) << "\t";
                cout << BLUE(ROUND(*counts, 0)) << "\t";
                print({ sum_ai, sum_pl, hand_ai, hand_pl });

                if (Czy_przegral(gracz_AI)) {
                    cout << GREEN("\nYou win!") << endl;
                    cout << "\nYour total card value: " << Suma_oczek(gracz) << endl;
                    cout << "Total value of AI's hand: " << Suma_oczek(gracz_AI) << endl;
                    break;
                }

                if (stop_pl == 1 && stop_AI == 1)
                {
                    if (Suma_oczek(gracz) > Suma_oczek(gracz_AI))
                        cout << GREEN("\nYou win!") << endl;
                    else if (Suma_oczek(gracz) == Suma_oczek(gracz_AI))
                        cout << BROWN("\nDraw...") << endl;
                    else
                        cout << RED("\nYou lose!") << endl;
                }

            } while (!Koniec_partii(gracz_AI, gracz, stop_AI, stop_pl));
            break;
        case '3':
            break;
        }

    } while (znak != '3');

    return 0;
}