# Grouper
A DSL written for organizers of group projects to help create the best possible groups for all participants. Designed to have a simple syntax to specify participants
by their interests, experience, desired positions, etc. in the hope of solving the problem of bad groups for projects.
An example program looks like:
```
Header:
	GroupSize: 3
	Names: Robin,Jackie,John,Marcus,Evan,Sally
	Interests: Math,Chemistry,Biology,Politics,Media_Studies,English,History
	Positions: Leader,Communications,Head_of_Design

Body:
	Groupee Robin:
		DontWantToWorkWith: Sally,Evan
		WantToWorkWith: Jackie,John
	Groupee Evan:
		Interests:Math,Biology,Media_Studies
		Positions:Leader,Head_of_Design
		WantToWorkWith: Jackie,John
		DontWantToWorkWith: Marcus,Evan
	Groupee Jackie:
		Interests:English,History,Biology
		Positions:Communications,Head_of_Design
		WantToWorkWith: Marcus,Robin,Evan
		DontWantToWorkWith: John
	Groupee Marcus:
		Interests:Chemistry,Politics,Math
		DontWantToWorkWith:Jackie
	Groupee John:
		Positions:Leader
  Groupee Sally:
    Interests: Chemistry, Biology,Math
    WantToWorkWith: Evan, Jackie
```
This would return a result:
```
Group 1: Leader: Evan,Communications: Jackie,Head_of_Design: Sally. Possible topics: Biology
Group 2: Leader: John,Communivations: Marcus,Head_of_Design: Robin. Possible topics: Chemistry,Politics,Math
```
