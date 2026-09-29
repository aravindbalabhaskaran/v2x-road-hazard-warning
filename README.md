# v2x-road-hazard-warning
Cooperative V2X road-hazard warning prototype using vehicle traction events and camera-based road-condition detection.
# V2X Road Hazard Warning

A prototype system that uses vehicle behaviour, camera information and V2X communication to detect possible road hazards and warn other vehicles approaching the same location.

## What is the idea?

Imagine a car driving on a road.

The car suddenly loses traction because the road is slippery, covered with water, gravel, debris, or another low-grip condition.

The car's existing safety systems such as ESC, ABS and TCS can already detect and react to the vehicle losing traction.

But there is another question:

**What if this information could be shared with the vehicles behind it?**

This project explores that idea.

Instead of keeping the traction event only inside one vehicle, the event can be converted into a road-hazard message and shared with other vehicles using V2X communication.

If several vehicles experience similar problems at approximately the same location, the system can determine that the road itself may have a problem.

The following vehicles can then receive an early warning before reaching the affected area.

---

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

```text
Vehicle 1
    ↓
Loss of traction
    ↓
Reports location
    ↓
        Road hazard information
               ↓
Vehicle 2 ─────┤
Vehicle 3 ─────┤
Vehicle 4 ─────┘
               ↓
       Hazard confidence increases
               ↓
        Warning for approaching vehicles
