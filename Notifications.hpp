#pragma once
#include <string>

using namespace std;

enum class NotificationType { Confirmation, Waitlist, Availability };

class Notifications {
private:
    int id;
    int registration_id;
    NotificationType type;
    string canvas_message_id;
    string sent_date;

public:
    Notifications() = default;
    Notifications(int id, int registration_id, NotificationType type)
       id(id), registration_id(registration_id), type(type) {}

    int getId() const { return id; }
    int getRegistrationId() const { return registration_id; }
    NotificationType getType() const { return type; }
    auto getCanvasMessageId() const { return canvas_message_id; }
    string getSentDate() const { return sent_date; }

    void setCanvasMessageId(const string& msg_id) { canvas_message_id = msg_id; }
    void setSentDate(const string& date) { sent_date = date; }
};
