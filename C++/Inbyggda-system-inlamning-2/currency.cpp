#include <iostream>
#include <fstream>
#include <string>

using namespace std;

class Currency {
private:
    string name;
    float value;

public:
    Currency(){
        name = "";
        value = 0;
    }

    Currency(string name, float value){
        this->name = name;
        this->value = value;
    }

    string getName(){
        return name;
    }

    void setName(string name) {
        this->name = name;
    }

    float getValue(){
        return value;
    }

    void setValue(float value){
        this->value = value;
    }

    void printCurrTable(){
        printf("|%-15s|%15.3f|\n", this->name.c_str(), this->value);
    }

};

Currency* getCurrencies() {
    static Currency currencies[100] = {};

    ifstream inFile("valutor.txt"); // Öppnar filen "valutor.txt" för läsning

    if (inFile.is_open()) {
        string next_value;
        float curr_value;
        int index = 0;


        while (inFile >> next_value){
            inFile >> curr_value;

            currencies[index] = Currency(next_value, curr_value);
            index++;
            
        }
    } else {
        cerr << "Could not open file." << std::endl;
    }

    inFile.close(); // Stäng filen
    return currencies;
}

void printCurrencies(Currency* currencies){
    printf("%.*s\n", 33, "+---------------+---------------+");
    printf("|%-15s|%15s|\n", "Currencies", "Value SEK 'öre'");
    printf("%.*s\n", 33, "+===============+===============+");
    for (int i = 0; i < 100; i++) {
        if (currencies[i].getName().empty()) {
            // Avsluta loopen när vi når det första tomma namnet
            break;
        }
        currencies[i].printCurrTable();
        printf("%.*s\n", 33, "+---------------+---------------+");
    }
}

int main() {
    printCurrencies(getCurrencies());
    return 0;
}
