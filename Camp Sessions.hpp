#pragma once
#include <string>

using namespace std;

class CampSessions {
private:
    int id;
    string name;
    string start_date;
    string end_date;
    int capacity;

public:
    CampSessions() = default;
    CampSessions(int id, const string& name, const string& start, const string& end, int capacity)
        : id(id), name(name), start_date(start), end_date(end), capacity(capacity) {}

    int getId() const { return id; }
    string getName() const { return name; }
    string getStartDate() const { return start_date; }
    string getEndDate() const { return end_date; }
    int getCapacity() const { return capacity; }

    void setName(const string& name) { this->name = name; }
    void setDates(const string& start, const string& end) {