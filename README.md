## Abstract
RememPill - a web-app that can be used to notify elder people that may not be so proud of their memory about when they should take their medication using phone calls and text-to-speech dynamically created messages. Serves as well as a tool for their care taker so they can feel safe about their beloved ones. This application was developed by the two contributors as our hack for BostonHacks2019 in 22 hours of coding.

## Inspiration
Both me and my teammate have grandparents who suffer from either memory loss or Alzheimer's. In any case, people afflicted with memory health problems are always hard to take care of and need constant attention in order to take their medication on time. Most of the time this is extremely hard for the afflicted members and requires too much time. It can also be quite expensive in the case of professionals caregivers. Of course, there are cases where the elder needs the constant attention but there are lots of scenarios where the elder can function quite enough on their own. That's how we came up with the idea of RememPill, a way to ease the load on families and provide assistance to elder people.
## What it does
RememPill offers an online web application where caregivers or family members can keep a digital pill case for each of their loved elderly members. This digital pill case helps to keep tracks of the weekly pills an elder person needs to take, but also helps with restocking. The digital pill case keeps track of each pill's details like name, color, shape, size and when it needs to be received. It then proceeds to make a phone call to the elder's person phone, at the specified times, as a reminder for them to take their medication. It acts as a reminder both in a sense of an alarm but also by dynamically generating and giving a description of the pill according to the digital pill case. The phone call also requires the elder to type in a number as a verification which acts as a stronger incentive to actually perform the task of taking their medication rather than simply receiving the call.
## How I built it
This is a web application developed using Python and the Django Library. The development of the objects needed to maintain was done using django and the front end was developed using HTML 5, Bootstrap and Javascript. We have integrated ngrock to provide a usable URL instead of having our project accessible only through localhost. In addition, we integrated the Twilio Api in order to make calls to the elder party. We also scheduled the phone calls by using the Redis framework and the rqscheduler so we could automate the process of the reminders.

## Challenges I ran into
Scheduling the phone calls proved quite challenging. It was a hard framework without much documentation. In addition, since we were not very experienced with Django setting up the backend required some time as well. 

## Accomplishments that I'm proud of
We have managed to setup an interesting user experience that is simple yet effective. We have managed to set up a back end that keeps track of what it needs to keep track. We have integrated twilio sucessfully and also managed to generate dynamic messages for the elders which gives a sense of familiarity. 
## What I learned
Building an application from scratch. Managing my time. Discussing with mentors. Exploring different possibilities and alternatives. Improving myself when i think i cannot. 

## What's next for RememPill
Add an even better scheduler. Offer the option to family members to record voice messages which then can replayed. This will give a sense of interest on their part and will be familiar to the elder people.
