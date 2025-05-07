#include <iostream>
#include <string>
#include <vector>
#include "Families.hpp"
#include "Camp Sessions.hpp"
#include "Campers.hpp"
#include "Notifications.hpp"
#include "Registrations.hpp"

using namespace std;

void displayMenu() {
  cout << "\n=== STEM Summer Camp Registration System ===\n";
  cout << "1. Add New Family\n";
  cout << "2. Add Camper to Family\n";
  cout << "3. View Available Camp Sessions\n";
  cout << "4. Register Camper for Session\n";
  cout << "5. View Registrations\n";
  cout << "6. Exit\n";
  cout << "Enter your choice: ";
}

Families addNewFamily() {
  string name, email, phone;
    
  cout << "\nEnter Family Information\n";
  cout << "Family Name: ";
  getline(cin >> ws, name);
    
  cout << "Email: ";
  getline(cin, email);
    
  cout << "Phone (optional): ";
  getline(cin, phone);
    
  static int id = 1; // In a real application, this would be handled by the database
  return Families(id++, name, email, phone);
}

int main() {
  vector<Families> families;
  vector<Campers> campers;
  vector<CampSession> sessions;
  vector<Registration> registrations;
    
  int choice;
  bool running = true;
    
  while (running) {
    displayMenu();
    cin >> choice;
        
    switch (choice) {
      case 1: {
        Families newFamily = addNewFamily();
        families.push_back(newFamily);
        cout << "Family added successfully!\n";
        break;
    }
      case 2: {
        if (families.empty()) {
          cout << "Please add a family first.\n";
          break;
    }
                
        cout << "\nAvailable Families:\n";
        for (const auto& family : families) {
          cout << "ID: " << family.getId() << " - " << family.getName() << "\n";
    }
                
        int familyId;
        string firstName, lastName;
                
        cout << "Enter Family ID: ";
        cin >> familyId;
                
        cout << "Enter Camper's First Name: ";
        getline(cin >> ws, firstName);
                
        cout << "Enter Camper's Last Name: ";
        getline(cin, lastName);
                
        static int camperId = 1;
        Campers newCamper(camperId++, familyId, firstName, lastName);
        campers.push_back(newCamper);
        cout << "Camper added successfully!\n";
        break;
    }
      case 3: {
        if (sessions.empty()) {
          cout << "No camp sessions available at this time.\n";
       } else {
          cout << "\nAvailable Camp Sessions:\n";
        for (const auto& session : sessions) {
          cout << "ID: " << session.getId() << " - " << session.getName() << "\n";
          cout << "Dates: " << session.getStartDate() << " to " << session.getEndDate() << "\n";
          cout << "Capacity: " << session.getCapacity() << "\n\n";
          }
      }
        break;
  }
      case 4: {
        if (campers.empty() || sessions.empty()) {
          cout << "Please ensure there are campers and sessions available first.\n";
          break;
            }
                
          int camperId, sessionId;
                
          cout << "\nEnter Camper ID: ";
          cin >> camperId;
                
          cout << "Enter Session ID: ";
          cin >> sessionId;
                
            static int registrationId = 1;
            Registration newRegistration(registrationId++, camperId, sessionId, RegistrationStatus::Registered);
            registrations.push_back(newRegistration);
            cout << "Registration successful!\n";
            break;
      }
      case 5: {
        if (registrations.empty()) {
          cout << "No registrations found.\n";
        } else {
          cout << "\nCurrent Registrations:\n";
        for (const auto& reg : registrations) {
          cout << "Registration ID: " << reg.getId() << "\n";
          cout << "Camper ID: " << reg.getCamperId() << "\n";
          cout << "Session ID: " << reg.getSessionId() << "\n";
          cout << "Status: " << (reg.getStatus() == RegistrationStatus::Registered ?"Registered" : "Waitlisted") << "\n\n";
            }
        }
          break;
    }
      case 6: {
        running = false;
        cout << "Thank you for using the registration system!\n";
        break;
      }
      default: {
        cout << "Invalid choice. Please try again.\n";
        break;
      }
    }
  }
    
    return 0;
}
