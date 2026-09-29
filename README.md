# V2X Road Hazard Warning

A prototype system that uses vehicle behaviour, camera information and V2X communication to detect possible road hazards and warn other vehicles approaching the same location.

## What is the idea?

Imagine a car driving on a road.

The car suddenly loses traction because the road is slippery, covered with water, gravel, debris, or another low-grip condition.

Modern vehicles already use systems such as ESC, ABS and TCS to detect and respond to wheel slip and vehicle instability.

But there is another question:

**What if this information could be shared with the vehicles behind it?**

This project explores that idea.

Instead of keeping the traction event only inside one vehicle, the event can be converted into a road-hazard message and shared with other vehicles using V2X communication.

If several vehicles experience similar problems at approximately the same location, the system can determine that the road itself may have a problem.

The following vehicles can then receive an early warning before reaching the affected area.

Vehicle 1
    |
    v
Loss of traction
    |
    v
Reports location
    |
    v
Road hazard information
    |
    +----------------+
    |                |
    v                v
Vehicle 2          Vehicle 3
    |                |
    +--------+-------+
             |
             v
    Hazard confidence increases
             |
             v
Approaching vehicle receives warning

The objective is therefore not to replace the vehicle's existing safety systems.

Instead, the project acts as a cooperative information layer above them.

## Why is this useful?

A vehicle can detect that **it is** having a problem.

But one vehicle may not know whether the problem is caused by:

- The driver
- The vehicle
- The tyres
- The road surface
- Water
- Gravel
- Debris
- Another temporary road condition

When multiple independent vehicles experience similar events at the same location, the information becomes more useful.

For example:

Vehicle 1
    |
    v
Traction event
    |
    v
GPS location + timestamp
    |
    v
Shared road information
    |
    +-------- Vehicle 2
    |
    +-------- Vehicle 3
    |
    +-------- Vehicle 4
    |
    v
Repeated evidence
    |
    v
Higher hazard confidence
    |
    v
Warning for approaching vehicles

## How does it work?

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
Hazard aggregation
    |
    v
Spatial filtering
    |
    v
Time freshness filtering
    |
    v
Hazard score
    |
    v
Warning state

The camera pipeline provides additional information:

Camera image
    |
    v
Image processing
    |
    v
Road region extraction
    |
    v
Road condition analysis
    |
    v
Camera hazard evidence

Vehicle and camera evidence are then combined:

Vehicle evidence
       +
Camera evidence
       |
       v
Evidence fusion
       |
       v
Combined hazard confidence
       |
       v
Warning decision

## What does the current prototype do?

The current prototype simulates the main software architecture of the system.

It currently includes:

- Vehicle traction-event detection
- Structured traction-event creation
- GPS-based spatial correlation
- Time-based event freshness
- Hazard scoring
- Warning-state management
- Camera image processing
- Road-region analysis
- Camera hazard evidence
- Vehicle and camera evidence fusion
- Cooperative multi-vehicle simulation

The system is designed as a research and software prototype rather than a production vehicle safety system.

## Vehicle behaviour simulation

The first part of the system simulates vehicle dynamics information.

The prototype currently uses wheel-speed differences to estimate possible traction loss.

For example:

Vehicle speed
    +
Wheel speeds
    |
    v
Slip calculation
    |
    v
Slip threshold
    |
    +------ Normal
    |
    +------ Possible traction loss

The detector produces:

- Detection state
- Traction-loss intensity

In a real vehicle, this information could instead come from existing vehicle systems or appropriate vehicle-network signals, depending on the vehicle platform and available interfaces.

The current Python detector is therefore a simulation of the vehicle-dynamics event input.

## Traction event creation

When a meaningful traction event is detected, it is converted into a structured event.

Each event contains:

- Event ID
- Vehicle ID
- Timestamp
- Latitude
- Longitude
- Vehicle speed
- Event intensity
- Event duration

Example:

Vehicle V001
    |
    v
Traction event detected
    |
    +------ Location
    +------ Time
    +------ Speed
    +------ Intensity
    +------ Duration
    |
    v
Structured traction event

This makes the event suitable for later V2X communication.

## Hazard aggregation

A single traction event does not automatically mean that the road is hazardous.

For example, a vehicle may lose traction because of:

- Driver behaviour
- Sudden acceleration
- Tyre condition
- Vehicle-specific problems

Therefore, the system looks for repeated events near the same location.

The prototype considers:

- Number of nearby events
- Event intensity
- Event duration
- Event location
- Event age

Older events gradually lose influence.

This prevents a road hazard from remaining active forever after the road condition has changed.

## Spatial correlation

Events are associated with a geographic area.

If several vehicles report events within a defined distance of each other, they can be considered related evidence.

Example:

Vehicle 1
    |
    +---- Event
          Location A

Vehicle 2
    |
    +---- Event
          Location A + small distance

Vehicle 3
    |
    +---- Event
          Location A + small distance

The system combines these observations into a local hazard estimate.

The current prototype uses a configurable correlation radius.

## Time freshness

Road conditions can change.

A slippery surface may be cleaned.

Water may disappear.

Gravel may be removed.

Construction work may finish.

Therefore, old reports should not have the same importance as recent reports.

The prototype applies a time-decay mechanism so that older events gradually lose their influence.

Recent event
    |
    v
High influence

Older event
    |
    v
Lower influence

Expired event
    |
    v
Ignored

This allows the hazard state to adapt to changing road conditions.

## Hazard scoring

The system converts the available evidence into a hazard score between 0 and 100.

The score considers:

- Number of nearby events
- Event intensity
- Event duration
- Event freshness
- Spatial correlation

The current thresholds are prototype values used for demonstrating the concept.

They are not automotive safety standards or validated warning thresholds.

## Camera information

Vehicle dynamics are useful for detecting low-grip conditions, but the camera can provide additional context.

The camera pipeline can analyse visible road conditions such as:

- Road surface changes
- Water
- Gravel
- Debris
- Construction areas
- Lane changes or diversions
- Possible road damage
- Other visible abnormalities

The current prototype uses basic computer-vision processing rather than a trained machine-learning model.

The current processing includes:

- Image loading
- Image resizing
- Grayscale conversion
- Noise reduction
- Histogram equalisation
- Road-region extraction
- Edge-density analysis
- Brightness analysis

The current camera analysis is a prototype heuristic and should not be interpreted as a reliable real-world hazard classifier.

## Possible low-grip surface detection

Some hazards may not be visually obvious.

For example, a road may have a low-friction surface without a clearly visible object or obstacle.

In this case, vehicle behaviour can provide important evidence.

The system therefore treats the camera as an additional information source rather than relying only on visual detection.

For contamination such as oil or other invisible surface conditions, the system should describe the result as:

**Possible low-grip road surface**

rather than claiming that the camera has specifically detected oil.

## Evidence fusion

The project combines vehicle-dynamics evidence with camera evidence.

The current prototype gives more weight to vehicle evidence because traction behaviour provides a direct indication that the vehicle experienced a loss of grip.

Conceptually:

Vehicle evidence
       |
       | 65%
       v
     +
     |
     |---- Combined hazard evidence
     |
     ^
     | 35%
       |
Camera evidence

The weights are prototype parameters and can be changed during future testing.

The goal is to investigate whether combining different sources of evidence can improve confidence in the estimated road condition.

## Cooperative multi-vehicle detection

The key part of the project is cooperation between vehicles.

Consider the following example:

Vehicle 1
    |
    v
Experiences traction loss
    |
    v
Reports event

Vehicle 2
    |
    v
Experiences similar traction loss
    |
    v
Reports event

Vehicle 3
    |
    v
Experiences similar traction loss
    |
    v
Reports event

Vehicle 4
    |
    v
Experiences similar traction loss
    |
    v
Reports event

The system receives repeated reports from approximately the same area.

As evidence increases:

WHITE
    |
    | additional evidence
    v
YELLOW
    |
    | strong additional evidence
    v
RED

This demonstrates the main cooperative concept.

## Warning states

The prototype uses three warning states.

### WHITE

No sufficiently strong road-hazard evidence.

The vehicle continues normally.

No warning beep is generated.

### YELLOW

There is enough repeated or meaningful evidence to indicate a possible road hazard.

A single warning beep is generated when the system transitions into YELLOW.

The system does not continuously beep while remaining in YELLOW.

### RED

The evidence indicates a stronger or higher-confidence road hazard.

A single warning beep is generated when the system transitions from YELLOW to RED.

The system does not continuously beep while remaining in RED.

The state can later decrease when evidence becomes old or the hazard is no longer supported.

## Warning behaviour

The prototype uses transition-based warnings.

Example:

WHITE -> WHITE
No beep

WHITE -> YELLOW
Beep

YELLOW -> YELLOW
No beep

YELLOW -> RED
Beep

RED -> RED
No beep

RED -> YELLOW
No beep

YELLOW -> WHITE
No beep

This prevents repeated warnings from becoming annoying while still notifying the driver when the hazard level increases.

## Example scenario

Imagine a road with unexpected water after heavy rain.

Vehicle 1 drives through the affected area.

The vehicle experiences wheel slip.

The event is recorded with:

- GPS location
- Timestamp
- Vehicle speed
- Traction intensity
- Event duration

The event is shared with the cooperative hazard system.

A few minutes later, Vehicle 2 passes through approximately the same location and experiences another traction event.

Vehicle 3 experiences the same problem.

The system now has several independent observations.

The hazard confidence increases.

An approaching vehicle can receive a warning before entering the affected area.

The warning could conceptually be:

**Possible low-grip road surface ahead**

This is different from the vehicle's own ESC or traction-control response.

ESC/TCS:
    |
    v
Protect the current vehicle

V2X hazard system:
    |
    v
Share information about the road
with other vehicles

## How V2X fits into the project

The current prototype simulates the cooperative communication concept in software.

A real implementation could use communication technologies such as:

- V2V
- V2I
- C-V2X
- ITS-G5
- MQTT or another suitable communication layer for a prototype environment

The exact communication technology would depend on the target deployment environment.

The important concept is that the vehicle event is converted into a standardized hazard message that can be understood by other vehicles.

Conceptually:

Vehicle
    |
    v
Traction event
    |
    v
Hazard message
    |
    v
V2X communication
    |
    +------ Vehicle 2
    +------ Vehicle 3
    +------ Vehicle 4
    |
    v
Cooperative hazard estimation

## What this project is NOT

This project does not attempt to replace:

- ESC
- ABS
- TCS
- Vehicle stability control
- Existing braking systems
- Existing vehicle safety ECUs

Those systems already perform safety-critical vehicle-control functions.

The purpose of this project is different.

Existing vehicle systems answer:

**"Is my vehicle losing traction, and how should I respond?"**

This project asks:

**"Did this vehicle experience a meaningful traction event that may indicate a road-condition problem, and should this information be shared with following vehicles?"**

Therefore, the proposed architecture is:

Existing vehicle dynamics / ESC event
            |
            v
     Event recording
            |
            +------ GPS
            +------ Timestamp
            +------ Intensity
            +------ Duration
            |
            v
    V2X hazard information
            |
            v
    Cooperative hazard estimation
            |
            v
    Warning for approaching vehicles

## Current implementation

The current prototype is implemented in Python.

Main technologies:

- Python
- NumPy
- Pandas
- OpenCV
- Pydantic
- Matplotlib
- Pytest
- Git
- GitHub

The project currently includes unit tests for the main components.

## Project structure

    v2x-road-hazard-warning/
    |
    +-- src/
    |   |
    |   +-- camera/
    |   |   +-- camera_processor.py
    |   |   +-- road_analyzer.py
    |   |   +-- camera_evidence.py
    |   |
    |   +-- detection/
    |   |   +-- traction_detector.py
    |   |
    |   +-- events/
    |   |   +-- hazard_event.py
    |   |   +-- event_factory.py
    |   |
    |   +-- hazards/
    |       +-- hazard_aggregator.py
    |       +-- warning_manager.py
    |       +-- evidence_fusion.py
    |
    +-- test_traction_detector.py
    +-- test_event.py
    +-- test_event_factory.py
    +-- test_hazard_aggregator.py
    +-- test_warning_manager.py
    +-- test_camera_processor.py
    +-- test_road_analyzer.py
    +-- test_camera_evidence.py
    +-- test_evidence_fusion.py
    +-- test_full_pipeline.py
    +-- test_cooperative_hazard.py
    |
    +-- requirements.txt
    +-- README.md
    +-- LICENSE

## Current prototype pipeline

The complete prototype can be represented as:

Vehicle behaviour
       |
       v
Traction detection
       |
       v
Traction event
       |
       +------ GPS
       +------ Timestamp
       +------ Speed
       +------ Intensity
       +------ Duration
       |
       v
Local hazard aggregation
       |
       +------ Spatial filtering
       +------ Time freshness
       +------ Event evidence
       |
       v
Vehicle hazard score
       |
       |
Camera image
       |
       v
Camera processing
       |
       v
Road analysis
       |
       v
Camera hazard evidence
       |
       +------------------+
                          |
                          v
                   Evidence fusion
                          |
                          v
                Combined hazard score
                          |
                          v
                  Warning state
                          |
                          v
                Driver notification

## Cooperative example

The current prototype demonstrates a simulated multi-vehicle scenario.

Example:

Vehicle 1 -> traction event
    |
    v
WHITE

Vehicle 2 -> similar nearby event
    |
    v
YELLOW + beep

Vehicle 3 -> similar nearby event
    |
    v
YELLOW, no additional beep

Vehicle 4 -> strong additional evidence
    |
    v
RED + beep

This demonstrates how repeated observations can increase confidence in a localized road hazard.

## Future development

Possible future improvements include:

- Unique-vehicle diversity weighting
- More realistic vehicle-dynamics signals
- Simulated V2V message exchange
- Standardized V2X message formats
- MQTT-based communication prototype
- Real GPS integration
- Real vehicle-network/CAN integration where appropriate
- Real test-vehicle validation
- Better road-surface classification
- Machine-learning-based camera analysis
- Pothole and road-damage detection
- Weather and environmental information
- Map-based hazard visualization
- More advanced spatial clustering
- Improved hazard confidence estimation
- Historical road-condition analysis
- Real-world validation using controlled test scenarios

## Research question

The project can be summarized by the following research question:

**Can repeated, geo-temporally correlated vehicle traction events be used to estimate and communicate localized road-friction hazards before following vehicles encounter the same condition?**

The prototype provides a software environment for exploring this question.

## Potential real-world application

A future system could operate as a cooperative road-condition information layer.

For example:

Vehicle A experiences low grip
        |
        v
Event recorded
        |
        v
Location + time + severity
        |
        v
V2X message
        |
        v
Cloud / edge / direct V2V infrastructure
        |
        +----------+
        |          |
        v          v
Vehicle B      Vehicle C
        |          |
        +-----+----+
              |
              v
      Local hazard information
              |
              v
     Early driver warning

This could potentially help vehicles receive information about temporary road conditions before directly encountering them.

## Disclaimer

This project is a research and software prototype.

The algorithms, thresholds and warning logic have not been validated for safety-critical automotive use.

The current traction detection, camera analysis and hazard thresholds are experimental and intended for demonstration and further research.

A production implementation would require extensive testing, validation, automotive-grade hardware and software processes, cybersecurity measures, communication standards, functional-safety considerations and controlled real-world testing.

## Author

**Aravind Balabhaskaran**

Master of Engineering – Engineering and Sustainable Technology Management  
Mobility and Automotive Industry

GitHub:
https://github.com/aravindbalabhaskaran

Project:
https://github.com/aravindbalabhaskaran/v2x-road-hazard-warning
