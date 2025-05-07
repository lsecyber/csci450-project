#pragma once
#include <string>

using namespace std;

enum class RegistrationStatus { Registered, Waitlisted };

class Registrations {
private:
    int id;
    int camper_id;
    int session_id;
    RegistrationStatus status;
    int waitlist_position;
    string registered_date;

public:
    Registrations() = default;
    Registrations(int id, int camper_id, int session_id, RegistrationStatus status)
        : id(id), camper_id(camper_id), session_id(session_id), status(status) {}

    int getId() const { return id; }
    int getCamperId() const { return camper_id; }
    int getSessionId() const { return session_id; }
    RegistrationStatus getStatus() const { return status; }
    auto getWaitlistPosition() const { return waitlist_position; }
    string getRegisteredDate() const { return registered_date; }

    void setStatus(RegistrationStatus s) { status = s; }
    void setWaitlistPosition(int pos) { waitlist_position = pos; }
    void setRegisteredDate(const string& date) { registered_date = date; }
};