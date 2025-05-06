#pragma once
#include <string>

using namespace std;

class Families {
private:
    int id;
    string name;
    string email;
    string phone;

public:
    Families() = default;
    Families(int id, const string& name, const string& email, const string& phone = "")
        : id(id), name(name), email(email), phone(phone) {}

    int getId() const { return id; }
    string getName() const { return name; }
    string getEmail() const { return email; }
    string getPhone() const { return phone; }

    void setName(const string& name) { this->name = name; }
    void setEmail(const string& email) { this->email = email; }
    void setPhone(const string& phone) { this->phone = phone; }
};
