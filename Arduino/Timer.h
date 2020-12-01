/*
 *      This program is free software; you can redistribute it and/or modify
 *      it under the terms of the GNU General Public License as published by
 *      the Free Software Foundation; either version 2 of the License, or
 *      (at your option) any later version.
 *
 *      This program is distributed in the hope that it will be useful,
 *      but WITHOUT ANY WARRANTY; without even the implied warranty of
 *      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *      GNU General Public License for more details.
 *
 *      You should have received a copy of the GNU General Public License
 *      along with this program; if not, write to the Free Software
 *      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *      MA 02110-1301, USA.
 */

/*  * * * * * * * * * * * * * * * * * * * * * * * * * * *
 Code by Simon Monk
 http://www.simonmonk.org
* * * * * * * * * * * * * * * * * * * * * * * * * * * * */

#ifndef Timer_h
#define Timer_h

#include <inttypes.h>
#include "Event.h"
#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

template<int numberOfEvents_> class Timer {

public:
  Timer(void);

  int8_t every(int32_t period, timerCallback_t callback, uint8_t id);
  int8_t every(int32_t period, timerCallback_t callback);
  int8_t after(int32_t duration, timerCallback_t callback, uint8_t id);
  int8_t after(int32_t duration, timerCallback_t callback);
  
  void stop(int8_t id);
  
  void update(void);
  void update(unsigned long now);

protected:
  static const int numberOfEvents= numberOfEvents_;
  Event _events[numberOfEvents_];
  int8_t findFreeEventIndex(void);

};

template<int numberOfEvents_> Timer<numberOfEvents_>::Timer(void) {
}

template<int numberOfEvents_> int8_t Timer<numberOfEvents_>::every(int32_t period, timerCallback_t callback, uint8_t id) {
	int8_t i = findFreeEventIndex();
	if (i == -1) return -1;

	_events[i].period = period;
	_events[i].eventType = EVENT_EVERY;
	_events[i].callback = callback;
	_events[i].lastEventTime = millis();
	_events[i].id= id;
	
	return i;
}

template<int numberOfEvents_> int8_t Timer<numberOfEvents_>::every(int32_t period, timerCallback_t callback) {
  every(period, callback, 0);
}

template<int numberOfEvents_> int8_t Timer<numberOfEvents_>::after(int32_t period, timerCallback_t callback, uint8_t id) {
	int8_t i = findFreeEventIndex();
	if (i == -1) return -1;

	_events[i].period = period;
	_events[i].eventType = EVENT_AFTER;
	_events[i].callback = callback;
	_events[i].lastEventTime = millis();
	_events[i].id= id;
	
	return i;
}

template<int numberOfEvents_> int8_t Timer<numberOfEvents_>::after(int32_t period, timerCallback_t callback) {
  after(period, callback, 0);
}

template<int numberOfEvents_> void Timer<numberOfEvents_>::stop(int8_t id) {
	if (id >= 0 && id < numberOfEvents) {
		_events[id].eventType = EVENT_NONE;
	}
}

template<int numberOfEvents_> void Timer<numberOfEvents_>::update(void) {
	unsigned long now = millis();
	update(now);
}

template<int numberOfEvents_> void Timer<numberOfEvents_>::update(unsigned long now) {
	for (int8_t i = 0; i < numberOfEvents; i++) {
		if (_events[i].eventType) {
			_events[i].update(now);
		}
	}
}

template<int numberOfEvents_> int8_t Timer<numberOfEvents_>::findFreeEventIndex(void) {
	for (int8_t i = 0; i < numberOfEvents; i++) {
		if (!_events[i].eventType) {
			return i;
		}
	}
	return -1;
}

#endif
