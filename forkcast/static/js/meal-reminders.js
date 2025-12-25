/**
 * Forkcast Meal Reminder Service
 * 
 * This script handles real-time meal reminders across all pages.
 * Works with GMT+6 timezone and persists settings in localStorage.
 */

(function() {
    'use strict';

    // Configuration
    const TIMEZONE_OFFSET = 6; // GMT+6
    const CHECK_INTERVAL = 30000; // Check every 30 seconds
    const REMINDER_WINDOW = 3; // 3 minute window to trigger reminder

    // State
    let settings = null;
    let reminderCheckInterval = null;
    let triggeredReminders = new Set();
    let notificationSound = null;
    let isInitialized = false;

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        if (isInitialized) return;
        isInitialized = true;

        console.log('[MealReminders] Initializing...');
        
        loadSettings();
        loadTriggeredReminders();
        initNotificationSound();
        requestNotificationPermission();
        startReminderChecker();
        scheduleMidnightReset();
        
        console.log('[MealReminders] Initialized with settings:', settings);
    }

    // Get current time in GMT+6
    function getGMT6Time() {
        const now = new Date();
        // Get UTC time and add 6 hours for GMT+6
        const utcTime = now.getTime() + (now.getTimezoneOffset() * 60000);
        const gmt6Time = new Date(utcTime + (TIMEZONE_OFFSET * 3600000));
        return gmt6Time;
    }

    // Get current time in minutes (for GMT+6)
    function getCurrentTimeInMinutes() {
        const gmt6 = getGMT6Time();
        return gmt6.getHours() * 60 + gmt6.getMinutes();
    }

    // Format time for display
    function formatTime(hours, minutes) {
        return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
    }

    // Load settings from localStorage or use defaults
    function loadSettings() {
        const savedSettings = localStorage.getItem('mealReminderSettings');
        if (savedSettings) {
            try {
                settings = JSON.parse(savedSettings);
                console.log('[MealReminders] Loaded settings from localStorage');
            } catch (e) {
                console.error('[MealReminders] Error parsing settings:', e);
                settings = getDefaultSettings();
            }
        } else {
            settings = getDefaultSettings();
            console.log('[MealReminders] Using default settings');
        }
        
        // Ensure reminders_enabled defaults to true
        if (settings.reminders_enabled === undefined || settings.reminders_enabled === null) {
            settings.reminders_enabled = true;
        }
    }

    // Default settings
    function getDefaultSettings() {
        return {
            reminders_enabled: true,
            breakfast_time: '08:00',
            lunch_time: '12:00',
            dinner_time: '18:00',
            snack_time: '15:00',
            breakfast_reminder_minutes: 0,
            lunch_reminder_minutes: 0,
            dinner_reminder_minutes: 0,
            snack_reminder_minutes: 0,
            sound_enabled: true
        };
    }

    // Load triggered reminders from localStorage
    function loadTriggeredReminders() {
        const saved = localStorage.getItem('triggeredRemindersToday');
        if (saved) {
            try {
                const data = JSON.parse(saved);
                const gmt6 = getGMT6Time();
                if (data.date === gmt6.toDateString()) {
                    triggeredReminders = new Set(data.reminders);
                    console.log('[MealReminders] Loaded triggered reminders:', triggeredReminders);
                } else {
                    // New day, clear reminders
                    triggeredReminders = new Set();
                    saveTriggeredReminders();
                }
            } catch (e) {
                triggeredReminders = new Set();
            }
        }
    }

    // Save triggered reminders to localStorage
    function saveTriggeredReminders() {
        const gmt6 = getGMT6Time();
        localStorage.setItem('triggeredRemindersToday', JSON.stringify({
            date: gmt6.toDateString(),
            reminders: Array.from(triggeredReminders)
        }));
    }

    // Initialize notification sound
    function initNotificationSound() {
        notificationSound = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2teleVIcNpTqvJJbLRhJqOC6e0gZNaPhsXpOMj1Lp9yxbzAlTqfZoWQ5O0um1plXNzhOqMqML0tAabTPdy0xPXLPvWchIj6Q1apOERQ7pNiZQgAIMqPiilkAAPFAn+uDUwD/qDed74xL/9OfMqjtj0n/qpAzsfGGRf/ZgzrD34VG/9J8R9ryhEr/x3td+OKDT//AfXXuxHZw/6yJi++2b4j/npeU7axuk/+RoJnxp22Z/4mmo/Wka5z/g6im+aFpnf9+q6n7nmie/3msq/udaJ//dq6s/Jxon/90r639m2if/3Kvrf2baKD/cq+u/Ztonv9yr679mmig/3Kvrf2aaJ//ca+t/Ztonv9xr679mmig/3Gvrf2aaKD/cq+t/Zpon/9yr679mmig/3Kvrf2aaJ//ca6t/Ztonv9xr679mmif/3Gvrf2aaKD/ca+t/Ztonv9xr679mmig/3Gvrf2aaKD/ca+t/Zton/9xr679mmif/3Gvrf2aaKD/ca+t/Zpon/9yr679mmig/3Kvrv2aaJ//cq+u/Zpon/9yr639mmig/3Kvrv2aaJ//cq+t/Zpon/9yr679mmig/3Kurv2aaJ//cq+t/Zpoof9yr679mmig/3Gvrf2aaKD/ca+t/Zponv9xr679mmig/3Gvrf2aaJ//ca+t/Zpon/9xr639mmig/3Gvrf2aaKD/ca+t/Zponv8=');
    }

    // Play notification sound
    function playNotificationSound() {
        if (settings && settings.sound_enabled !== false && notificationSound) {
            notificationSound.currentTime = 0;
            notificationSound.play().catch(e => console.log('[MealReminders] Could not play sound:', e));
        }
    }

    // Request browser notification permission
    function requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission().then(permission => {
                console.log('[MealReminders] Notification permission:', permission);
            });
        }
    }

    // Start the reminder checker
    function startReminderChecker() {
        console.log('[MealReminders] Starting reminder checker...');
        
        // Check immediately
        checkMealReminders();
        
        // Then check periodically
        if (reminderCheckInterval) {
            clearInterval(reminderCheckInterval);
        }
        reminderCheckInterval = setInterval(checkMealReminders, CHECK_INTERVAL);
    }

    // Schedule reset at midnight GMT+6
    function scheduleMidnightReset() {
        const gmt6 = getGMT6Time();
        const tomorrow = new Date(gmt6);
        tomorrow.setDate(tomorrow.getDate() + 1);
        tomorrow.setHours(0, 0, 0, 0);
        
        const msUntilMidnight = tomorrow - gmt6;
        
        setTimeout(() => {
            console.log('[MealReminders] Midnight reset - clearing triggered reminders');
            triggeredReminders.clear();
            saveTriggeredReminders();
            scheduleMidnightReset();
        }, msUntilMidnight);
    }

    // Check if any meal reminders should be triggered
    function checkMealReminders() {
        // Reload settings in case they were updated
        loadSettings();
        
        if (!settings || settings.reminders_enabled === false) {
            return;
        }

        const gmt6 = getGMT6Time();
        const currentTime = getCurrentTimeInMinutes();
        
        console.log(`[MealReminders] Checking at GMT+6 ${formatTime(gmt6.getHours(), gmt6.getMinutes())} (${currentTime} minutes)`);
        
        const meals = [
            { type: 'breakfast', time: settings.breakfast_time, reminderMinutes: settings.breakfast_reminder_minutes || 0 },
            { type: 'lunch', time: settings.lunch_time, reminderMinutes: settings.lunch_reminder_minutes || 0 },
            { type: 'dinner', time: settings.dinner_time, reminderMinutes: settings.dinner_reminder_minutes || 0 },
            { type: 'snack', time: settings.snack_time, reminderMinutes: settings.snack_reminder_minutes || 0 }
        ];

        meals.forEach(meal => {
            if (!meal.time) return;
            
            const [hours, minutes] = meal.time.split(':').map(Number);
            const mealTimeMinutes = hours * 60 + minutes;
            const reminderTimeMinutes = mealTimeMinutes - meal.reminderMinutes;
            
            const reminderKey = `${meal.type}-${gmt6.toDateString()}`;
            const isInWindow = currentTime >= reminderTimeMinutes && currentTime < reminderTimeMinutes + REMINDER_WINDOW;
            const alreadyTriggered = triggeredReminders.has(reminderKey);
            
            console.log(`[MealReminders] ${meal.type}: meal=${meal.time}, reminderAt=${formatTime(Math.floor(reminderTimeMinutes/60), reminderTimeMinutes%60)}, inWindow=${isInWindow}, triggered=${alreadyTriggered}`);
            
            if (isInWindow && !alreadyTriggered) {
                console.log(`[MealReminders] Triggering ${meal.type} reminder!`);
                triggeredReminders.add(reminderKey);
                saveTriggeredReminders();
                triggerMealReminder(meal.type, meal.time, meal.reminderMinutes);
            }
        });
    }

    // Trigger a meal reminder
    function triggerMealReminder(mealType, mealTime, minutesBefore) {
        const mealNames = {
            breakfast: 'Breakfast',
            lunch: 'Lunch',
            dinner: 'Dinner',
            snack: 'Snack'
        };
        
        const mealEmojis = {
            breakfast: '🌅',
            lunch: '☀️',
            dinner: '🌙',
            snack: '🍎'
        };
        
        const title = `${mealEmojis[mealType] || '🍽️'} ${mealNames[mealType]} Reminder`;
        const message = `It's almost time for ${mealNames[mealType].toLowerCase()}! Your meal is scheduled for ${mealTime}.`;
        
        // Play sound
        playNotificationSound();
        
        // Show browser notification
        if ('Notification' in window && Notification.permission === 'granted') {
            const notification = new Notification(title, {
                body: message,
                icon: '/static/images/logo.png',
                tag: `meal-${mealType}`,
                requireInteraction: true
            });
            
            notification.onclick = () => {
                window.focus();
                window.location.href = '/calendar';
                notification.close();
            };
        }
        
        // Show in-page toast notification
        showMealReminderToast(title, message, mealType);
        
        // Save to database if user is logged in
        saveReminderToDatabase(mealType, mealTime);
    }

    // Show in-page toast notification
    function showMealReminderToast(title, message, mealType) {
        // Remove any existing toast
        const existingToast = document.getElementById('meal-reminder-toast');
        if (existingToast) {
            existingToast.remove();
        }

        const mealEmojis = {
            breakfast: '🌅',
            lunch: '☀️',
            dinner: '🌙',
            snack: '🍎'
        };
        
        const toast = document.createElement('div');
        toast.id = 'meal-reminder-toast';
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            max-width: 400px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 16px;
            z-index: 99999;
            border-left: 4px solid #4A7C59;
            animation: slideInRight 0.3s ease-out;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        `;
        
        toast.innerHTML = `
            <style>
                @keyframes slideInRight {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOutRight {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
            </style>
            <div style="display: flex; align-items: flex-start; gap: 12px;">
                <div style="font-size: 32px;">${mealEmojis[mealType] || '🍽️'}</div>
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 4px 0; font-weight: 600; color: #3D405B; font-size: 16px;">${escapeHtml(title)}</h4>
                    <p style="margin: 0 0 12px 0; color: #666; font-size: 14px;">${escapeHtml(message)}</p>
                    <div style="display: flex; gap: 8px;">
                        <a href="/calendar" style="padding: 6px 12px; background: #4A7C59; color: white; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 500;">
                            View Meal Plan
                        </a>
                        <button onclick="this.closest('#meal-reminder-toast').remove()" style="padding: 6px 12px; background: #f3f4f6; color: #374151; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">
                            Dismiss
                        </button>
                    </div>
                </div>
                <button onclick="this.closest('#meal-reminder-toast').remove()" style="background: none; border: none; cursor: pointer; color: #9ca3af; font-size: 18px; padding: 0; line-height: 1;">×</button>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-remove after 30 seconds
        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.animation = 'slideOutRight 0.3s ease-out forwards';
                setTimeout(() => toast.remove(), 300);
            }
        }, 30000);
    }

    // Escape HTML
    function escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Save reminder to database (only if logged in)
    async function saveReminderToDatabase(mealType, mealTime) {
        try {
            const response = await fetch('/notifications/api/create-meal-reminder', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    meal_type: mealType,
                    meal_time: mealTime
                })
            });
            
            if (response.ok) {
                console.log('[MealReminders] Reminder saved to database');
            }
        } catch (error) {
            // User might not be logged in, that's okay
            console.log('[MealReminders] Could not save to database (user may not be logged in)');
        }
    }

    // Expose functions globally for manual testing
    window.MealReminders = {
        test: function() {
            const mealTypes = ['breakfast', 'lunch', 'dinner', 'snack'];
            const randomMeal = mealTypes[Math.floor(Math.random() * mealTypes.length)];
            const gmt6 = getGMT6Time();
            const testTime = formatTime(gmt6.getHours(), gmt6.getMinutes());
            triggerMealReminder(randomMeal, testTime, 0);
            console.log('[MealReminders] Test reminder triggered');
        },
        scheduleQuick: function() {
            const gmt6 = getGMT6Time();
            const futureTime = new Date(gmt6.getTime() + 60000);
            const reminderTime = formatTime(futureTime.getHours(), futureTime.getMinutes());
            
            settings.breakfast_time = reminderTime;
            settings.breakfast_reminder_minutes = 0;
            
            const today = gmt6.toDateString();
            triggeredReminders.delete(`breakfast-${today}`);
            saveTriggeredReminders();
            
            // Save to localStorage so it persists
            localStorage.setItem('mealReminderSettings', JSON.stringify(settings));
            
            console.log(`[MealReminders] Quick reminder scheduled for ${reminderTime} GMT+6`);
            alert(`Reminder scheduled for ${reminderTime} GMT+6 (in ~1 minute). Keep this page open!`);
        },
        getSettings: function() {
            return settings;
        },
        getGMT6Time: function() {
            const gmt6 = getGMT6Time();
            return formatTime(gmt6.getHours(), gmt6.getMinutes());
        },
        reload: function() {
            loadSettings();
            // Clear triggered reminders so new times can trigger
            triggeredReminders.clear();
            saveTriggeredReminders();
            console.log('[MealReminders] Settings reloaded and reminders cleared:', settings);
        },
        checkNow: function() {
            checkMealReminders();
        }
    };

    console.log('[MealReminders] Service loaded. Use MealReminders.test() to test, MealReminders.getGMT6Time() to see current time.');
})();
