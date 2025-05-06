#pragma once
#include <string>

using namespace std;

enum class Gender { Male, Female, Other };

class Campers {
private:
    int id;
    int family_id;
    string first_name;
    string last_name;
    string dob;
    string gender;

public:
    Camper() = default;
    Camper(int id, int family_id, const string& first_name, const string& last_name)
        : id(id), family_id(family_id), first_name(first_name), last_name(last_name) {}

    int getId() const { return id; }
    int getFamilyId() const { return family_id; }
    string getFirstName() const { return first_name; }
    string getLastName() const { return last_name; }
    auto getDob() const { return dob; }
    auto getGender() const { return gender; }

    void setNames(const string& first, const string& last) {
        first_name = first;
        last_name = last;
    }
    void setDob(const string& date) { dob = date; }
    void setGender(Gender g) { gender = g; }
};