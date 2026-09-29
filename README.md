# V2X Road Hazard Warning

A prototype system for detecting possible road hazards from vehicle behaviour and camera information, sharing the information between vehicles, and generating warnings for vehicles approaching the affected location.

The main idea is simple:

**One vehicle experiences a problem → reports it → other vehicles contribute information → the system estimates whether the road itself may be hazardous → approaching vehicles receive a warning.**

---

## What is the idea?

Imagine a vehicle driving normally on a road.

Suddenly, the vehicle experiences unexpected loss of traction.

This could happen because of:

- Water on the road
- A slippery road surface
- Gravel
- Loose material
- Debris
- Snow or ice
- Temporary road conditions
- Other low-grip conditions

Modern vehicles already have safety systems such as **ESC, ABS and TCS** that can detect and respond to wheel slip or vehicle instability.

These systems are designed primarily to help the **current vehicle** remain stable and safe.

This project explores another question:

> **Can useful information from one vehicle be shared with other vehicles to warn them about a possible road problem before they reach the same location?**

The project uses vehicle events, location and camera information to create a shared road-hazard picture.

---

## Why is this useful?

A single traction event does not necessarily mean that the road is dangerous.

The event could have been caused by:

- Driver behaviour
- Vehicle behaviour
- Tyre condition
- A temporary manoeuvre
- The road surface
- Water
- Gravel
- Debris
- Another local road condition

However, if several independent vehicles experience similar events at approximately the same location, the information becomes more meaningful.

For example:

```text
Vehicle 1
    |
    | Loss of traction
    v
Reports event + location
    |
    v
+---------------------------+
|   Shared Hazard Data      |
+---------------------------+
    ^
    |
Vehicle 2 ---- Loss of traction
Vehicle 3 ---- Loss of traction
Vehicle 4 ---- Loss of traction
    |
    v
Repeated events at same area
    |
    v
Hazard confidence increases
    |
    v
Approaching vehicle receives warning

The objective is therefore not to replace the vehicle's existing safety systems.

Instead, the project acts as a cooperative information layer above them.

```text

How does it work?

The prototype follows this general pipeline:

Vehicle behaviour
       |
       v
Traction event detection
       |
       v
Create vehicle event
       |
       +------ GPS location
       |
       +------ Timestamp
       |
       +------ Vehicle speed
       |
       +------ Event intensity
       |
       +------ Event duration
       |
       v
Road hazard aggregation
       |
       +------ Nearby events
       |
       +------ Number of vehicles
       |
       +------ Event intensity
       |
       +------ Location correlation
       |
       v
Camera evidence
       |
       +------ Road region
       +------ Brightness
       +------ Edge information
       |
       v
Evidence fusion
       |
       v
Hazard confidence
       |
       v
WHITE / YELLOW / RED
       |
       v
Driver warning
What does the current prototype do?

The current GitHub prototype is a software simulation of this concept.

It does not require a real vehicle or real V2X hardware.

Instead, vehicle sensor information is simulated using Python.

1. Vehicle behaviour simulation

The prototype simulates vehicle speed and wheel-speed information.

A simplified traction detector compares the vehicle speed with the wheel speeds and estimates whether a traction-loss event may have occurred.

Example:

Normal driving
    |
    +-- Wheel speeds approximately match vehicle speed
    |
    +-- No significant traction event

Possible traction loss
    |
    +-- Wheel speed differs significantly
    |
    +-- Traction event generated

The detector also produces an estimated event intensity between 0 and 1.

This detector is a prototype simulation and is not intended to replace a production ESC, ABS or TCS system.

2. Traction event creation

When a traction event is detected, the system creates a structured event.

The event contains information such as:

Event ID
Vehicle ID
Timestamp
Latitude
Longitude
Vehicle speed
Event intensity
Event duration

For example:

Vehicle: V001
Speed: 50 km/h
Intensity: 0.37
Duration: 1.5 seconds
Location: GPS coordinates
Time: UTC timestamp

This converts a vehicle behaviour event into information that can potentially be shared with other vehicles.

3. Hazard aggregation

A single vehicle report is not automatically treated as a confirmed road hazard.

The system collects events from multiple vehicles.

It checks whether events occur:

Close to each other geographically
Within a relevant time period
With meaningful intensity

The more supporting events there are, the higher the hazard score can become.

For example:

Vehicle 1
    |
    +-- Traction event
    |
    v

Vehicle 2
    |
    +-- Similar event
    |
    v

Vehicle 3
    |
    +-- Similar event
    |
    v

Same road area
    |
    v
Higher hazard confidence

This is the main cooperative part of the project.

4. Camera information

Vehicle behaviour is not the only source of information.

The prototype also includes a camera-processing component using OpenCV.

The camera module analyses the road region of an image and extracts basic visual information such as:

Image brightness
Edge density
Road-region information
Basic visual evidence

This is currently a prototype evidence-generation system.

The intention is that camera information can provide additional context around a vehicle event.

For example:

Vehicle loses traction
        +
Camera sees unusual road conditions
        |
        v
Stronger supporting evidence

The camera does not currently claim to identify specific materials such as oil or black ice.

Instead, it provides additional evidence that can contribute to the overall hazard assessment.

5. Evidence fusion

The project combines different sources of information.

Currently the main sources are:

Vehicle dynamics
       +
Camera evidence
       +
Cooperative vehicle reports
       |
       v
Combined hazard confidence

The idea is that no single sensor or vehicle should necessarily determine the road condition by itself.

Different sources can support each other.

6. Warning states

The prototype uses three warning states:

WHITE
YELLOW
RED
WHITE

Represents:

No sufficiently strong or corroborated hazard information yet.

A single weak or ambiguous event should not immediately create a strong warning.

YELLOW

Represents:

Possible or corroborated road hazard.

There is enough supporting evidence to indicate that approaching vehicles should be more aware of the road condition.

The prototype can generate a warning when the state changes from:

WHITE → YELLOW
RED

Represents:

Higher-confidence road hazard.

The system has received stronger evidence based on factors such as multiple events and event intensity.

The prototype can generate a stronger warning when the state changes from:

YELLOW → RED
Warning behaviour

The system is designed to avoid continuously beeping while the warning state remains unchanged.

For example:

WHITE → WHITE
Beep: No

WHITE → YELLOW
Beep: Yes

YELLOW → YELLOW
Beep: No

YELLOW → RED
Beep: Yes

RED → RED
Beep: No

This prevents the same warning from repeatedly alerting the driver.

The current thresholds are experimental prototype parameters and are not automotive safety standards.

Example scenario

Consider four vehicles travelling along the same road.

Vehicle 1

Vehicle 1 experiences a moderate traction event.

Vehicle 1
    |
    +-- Traction event
    +-- GPS location
    +-- Timestamp
    +-- Intensity

The system records the event.

The information is not yet considered strong enough to confidently classify the road as hazardous.

Vehicle 2

A few moments later, Vehicle 2 experiences a similar traction event near the same location.

Vehicle 1 ----+
              |
Vehicle 2 ----+---- Same road area
              |
              v
        Evidence increases

The hazard confidence increases.

The system may move to:

YELLOW
Vehicle 3

Vehicle 3 experiences another strong event at approximately the same location.

The system now has multiple independent reports.

Vehicle 1 ----+
Vehicle 2 ----+---- Same location
Vehicle 3 ----+
              |
              v
       Stronger evidence
              |
              v
             RED

An approaching vehicle can now receive a stronger road-hazard warning before reaching the affected area.

How V2X fits into the system

In the current prototype, V2X communication is simulated through software events.

A future real implementation could use appropriate V2X communication technologies and standardized messages.

Conceptually:

Vehicle A
    |
    | Hazard event
    v
V2X communication
    |
    v
Road hazard information
    |
    +----------------+
    |                |
    v                v
Vehicle B        Vehicle C
    |                |
    +-------+--------+
            |
            v
     Driver warning

The project therefore separates the idea of:

Detecting an event

from:

Sharing the event

and:

Understanding whether the event represents a road hazard.

What the project is NOT

This project is not intended to:

Replace ESC
Replace ABS
Replace TCS
Control the vehicle
Automatically steer the vehicle
Automatically brake the vehicle
Directly access proprietary vehicle ECUs
Claim that a specific road contaminant has been identified
Provide a production-ready automotive safety system

The current project is a research and software prototype demonstrating the concept of cooperative road-hazard detection.

Current implementation

The prototype is implemented in Python.

Main technologies include:

Python
NumPy
Pandas
Pydantic
OpenCV
Matplotlib
Pytest
Git / GitHub

The project contains separate modules for:

Vehicle behaviour detection
        |
        v
Event generation
        |
        v
Hazard aggregation
        |
        v
Camera processing
        |
        v
Camera evidence
        |
        v
Evidence fusion
        |
        v
Warning management
        |
        v
Cooperative hazard simulation
Project structure
v2x-road-hazard-warning/
│
├── src/
│   ├── camera/
│   │   ├── camera_evidence.py
│   │   ├── camera_processor.py
│   │   └── road_analyzer.py
│   │
│   ├── detection/
│   │   └── traction_detector.py
│   │
│   ├── events/
│   │   ├── event_factory.py
│   │   └── hazard_event.py
│   │
│   └── hazards/
│       ├── evidence_fusion.py
│       ├── hazard_aggregator.py
│       └── warning_manager.py
│
├── test_camera_evidence.py
├── test_camera_processor.py
├── test_cooperative_hazard.py
├── test_detection_to_event.py
├── test_event.py
├── test_event_factory.py
├── test_evidence_fusion.py
├── test_full_pipeline.py
├── test_hazard_aggregator.py
├── test_road_analyzer.py
├── test_traction_detector.py
├── test_warning_manager.py
│
├── requirements.txt
├── README.md
└── LICENSE
Current prototype pipeline

The complete software pipeline can currently be demonstrated as:

Simulated vehicle data
        ↓
Traction detection
        ↓
Traction event creation
        ↓
Vehicle hazard estimation
        ↓
Camera analysis
        ↓
Camera evidence
        ↓
Evidence fusion
        ↓
Cooperative hazard aggregation
        ↓
Warning state
        ↓
Driver warning

The prototype has been tested using simulated scenarios involving multiple vehicles.

Future development

The current GitHub project provides the software proof-of-concept.

The next stage would involve testing the concept with real vehicle and environmental data.

Possible future development includes:

Real vehicle data

Instead of simulated wheel speeds:

Real vehicle sensors
        ↓
CAN / vehicle interface
        ↓
Vehicle dynamics information
        ↓
Traction event

Actual access to vehicle ECU/CAN data would depend on the vehicle, manufacturer, interface and applicable safety/security restrictions.

Real camera data

A real forward-facing camera or dashcam could be used to collect road images and videos.

The system could then be developed to identify additional road conditions such as:

Potholes
Water accumulation
Road debris
Construction areas
Lane changes
Temporary diversions
Gravel
Snow or ice-related visual conditions

Computer vision and machine-learning models could be introduced after sufficient real data is available.

Real V2X communication

The simulated vehicle-to-vehicle communication could eventually be replaced by real V2X communication technologies.

The system could then allow vehicles to exchange road-hazard information in real time.

Real-world validation

A laboratory or test vehicle environment could be used to evaluate:

Detection accuracy
False positives
False negatives
GPS accuracy
Event correlation
Warning timing
Communication latency
Camera performance
Different road conditions
Different vehicle speeds

Safety-critical testing would need appropriate controlled environments, equipment, supervision and applicable automotive testing procedures.

Research question

The main research question behind this project is:

Can repeated, geo-temporally correlated vehicle traction events be used to estimate and communicate localized road-friction hazards to approaching vehicles?

The project explores how information that is normally useful only to one vehicle could become useful to an entire group of vehicles travelling through the same road environment.

Conclusion

The purpose of this project is to demonstrate the concept of cooperative road-hazard awareness.

A vehicle does not need to know everything about the road by itself.

Instead:

Vehicle behaviour
        +
Camera information
        +
Other vehicles
        +
Location and time
        |
        v
Shared understanding of road conditions
        |
        v
Earlier warning for approaching vehicles

The long-term goal is to move from:

"My vehicle detected a problem."

to:

"Vehicles are collectively building information about the road ahead."

Disclaimer

This is a research and software prototype.

The warning logic, thresholds and detection algorithms are experimental and are not intended for direct use in production vehicles or safety-critical systems.

Real-world deployment would require extensive validation, appropriate vehicle interfaces, V2X standards, cybersecurity measures, functional safety processes and controlled testing.


This version is much more suitable for a GitHub portfolio because someone looking at it can understand **what problem you're solving, how your software works, what is already implemented, and what would require a real vehicle/lab next**.
