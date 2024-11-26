# About
This subpackage contains the modules that define the components that make up the Model of MVC. Remember that the Model is a layer, not a concrete class. We define the Model to have 3 main components: Entities, Data Mappers, and Services.

## Entities
Entities are the classes that represent things in the problem domain. They encapsulate data and logic specific to that thing. Entities should be designed persistence-independent, meaning they need not know if/how they're stored. A proper Entity will contain all the logic for ensuring it is never in an invalid state (e.g. field with a bad type/value) and performing operations on itself to change its state.

## Data Mappers
Data Mappers are the classes that manage the storage and retrieval of Entities from data stores (CSV file, SQL database, etc.). Data Mappers should take in and return Entities, depending on how they interact (e.g. read, write) with the data store. Entities validate themselves, so there should be no need for validation by the Data Mapper. Its job is to simply persist an Entity to the data store or populate an Entity with its data as stored. 

## Services
Services are the classes that facilitate communication between the Controllers outside the Model and the Entities and Data Mappers inside. They should handle a specific interaction between the user (acting via a Controller) and related Entities/Data Mappers. That said, as Services are part of the Model, they should not be aware of or depend on components outside. Services take in a user request (abstracted in some way) as input and determine how to change the state of the Model by interacting with certain Data Mappers. In practice, Views will "observe" Services, meaning that after a Service has done its work, it will communicate the state of the Model to the View for futher processing (e.g. displaying an error message). Services can still exist without Views though.

# What is Model state?
It's complicated, and probably best understood through examples. Creating a new user and storing them in the database is a state change. Updating the number of likes on a blog post is a state change. An error arising from an Entity is a state change. In any case, it is the user acting through Controllers which call Services that result in a change to the Model's state.