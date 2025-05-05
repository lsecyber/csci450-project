// src/utils/tableHeaders.js
// This file defines the headers for various tables used in the application.

import { ref } from 'vue';

export const familiesHeaders = ref([
    { title: 'ID', key: 'id', align: 'start', sortable: false },
    { title: 'Name', key: 'name', align: 'start', sortable: true },
    { title: 'Email', key: 'email', align: 'start', sortable: true },
    { title: 'Phone', key: 'phone', align: 'start', sortable: true },
    { title: 'Created At', key: 'created_at', align: 'end', sortable: true, showInList: false },
    { title: 'Updated At', key: 'updated_at', align: 'end', sortable: true, showInList: false }
]);

export const sessionsHeaders = ref([
    { title: 'ID', key: 'id', align: 'start', sortable: false },
    { title: 'Name', key: 'name', align: 'start', sortable: true },
    { title: 'Start Date', key: 'start_date', align: 'end', sortable: true },
    { title: 'End Date', key: 'end_date', align: 'end', sortable: true },
    { title: 'Capacity', key: 'capacity', align: 'end', sortable: true },
    { title: 'Created At', key: 'created_at', align: 'end', sortable: true, showInList: false },
    { title: 'Updated At', key: 'updated_at', align: 'end', sortable: true, showInList: false }
]);

export const campersHeaders = ref([
    { title: 'ID', key: 'id', align: 'start', sortable: false },
    { title: 'Family ID', key: 'family_id', align: 'end', sortable: true },
    { title: 'First Name', key: 'first_name', align: 'start', sortable: true },
    { title: 'Last Name', key: 'last_name', align: 'start', sortable: true },
    { title: 'DOB', key: 'dob', align: 'end', sortable: true },
    { title: 'Gender', key: 'gender', align: 'start', sortable: true },
    { title: 'Created At', key: 'created_at', align: 'end', sortable: true, showInList: false },
    { title: 'Updated At', key: 'updated_at', align: 'end', sortable: true, showInList: false }
]);

export const registrationsHeaders = ref([
    { title: 'ID', key: 'id', align: 'start', sortable: false },
    { title: 'Camper ID', key: 'camper_id', align: 'end', sortable: true },
    { title: 'Session ID', key: 'session_id', align: 'end', sortable: true },
    { title: 'Status', key: 'status', align: 'start', sortable: true },
    { title: 'Waitlist Position', key: 'waitlist_position', align: 'end', sortable: true },
    { title: 'Registered At', key: 'registered_at', align: 'end', sortable: true, showInList: false },
    { title: 'Updated At', key: 'updated_at', align: 'end', sortable: true, showInList: false }
]);

export const notificationsHeaders = ref([
    { title: 'ID', key: 'id', align: 'start', sortable: false },
    { title: 'Registration ID', key: 'registration_id', align: 'end', sortable: true },
    { title: 'Type', key: 'type', align: 'start', sortable: true },
    { title: 'Canvas Msg ID', key: 'canvas_message_id', align: 'start', sortable: true },
    { title: 'Sent At', key: 'sent_at', align: 'end', sortable: true }
]);

const headersMap = {
    families: familiesHeaders,
    sessions: sessionsHeaders,
    campers: campersHeaders,
    registrations: registrationsHeaders,
    notifications: notificationsHeaders
};

/**
 * @param {string} tableName
 * @returns {import('vue').Ref<Array<Object>>}
 */
export function getTableHeaders(tableName) {
    // keys here are the routes/views names you used
    return headersMap[tableName] || ref([]);
}