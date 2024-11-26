# What is MVC?
MVC stands for Model, View, Controller. MVC is a software design pattern, and its main goal is to better separate the domain logic from the presentation logic.

## What is the Model?
Contrary to popular belief, the Model is not an individual class. Rather, it is an abstract layer meant to encapsulate domain and application logic. 

Domain (business) logic defines the real-life rules and operations specific to the problem at hand. For example, if you're developing a banking system, you'll need logic to handle happens when a customer misses a credit card payment or withdraw more money than they have in their bank account. This is true no matter how the system is actually implemented (web app, mobile app, executable program, etc.) - domain logic is reusable and system-indepedent. 

It is the application logic that defines how the particular system implementation will expose the domain logic to the user. If the system is a web app, then the application logic would define how to interact with the database, format a JSON or HTML response, authenticate with a username/password, etc. 

Naturally, the bulk of the system is defined in the Model. Given the encapsulation and blending of business and application logic, a well-designed Model will contain many components that do more than abstract database access or represent a table in a database.

## What is the View?
The View is ultimately what the user receives in response to an interaction with the system. The View is not merely an HTML template to be populated with data. The View could just as well respond with JSON or XML data, depending on who (or what) the user is. Instead, the View should encapsulate the logic for fetching data from the Model (layer), formatting it in some way (e.g. HTML, JSON), and returning a response to the user. In actuality, there is no singular View class - each specific response should have its own View.

## What is the Controller?
The Controller is what allows the user to interact with the Model and receive a response from the View. It should be relatively thin, simply initiating a state change in the Model and triggering the View to reflect those state changes to the user. Just like the View, there are actually many Controller classes, each of which is responsible for handling a specific interaction between the user, Model layer components, and a View. Picking the correct Controller to forward the user's request to is the job of what is commonly called the Front Controller.

# Where can I learn more about MVC?
There are many MVC frameworks that aim to simplify the implementation of the design pattern. Of course, everyone has their own take, and some are better than others. Before subscribing to a particular implementation's take, consider reading some of these StackOverflow posts below:
- [How should a model be structured in MVC?](https://stackoverflow.com/questions/5863870/how-should-a-model-be-structured-in-mvc/5864000#5864000)
- [What's the best approach to divide model and actions into classes in MVC pattern](https://stackoverflow.com/questions/51729687/whats-the-best-approach-to-divide-model-and-actions-into-classes-in-mvc-pattern/51735316#51735316)
- [How should a model be structured in MVC?](https://stackoverflow.com/questions/5863870/how-should-a-model-be-structured-in-mvc/5864000#5864000)
- [Using models in a controller alongside with repository](https://stackoverflow.com/questions/62615432/using-models-in-a-controller-alongside-with-repository/62617834#62617834)
- [PHP - Structuring a Slim3 web application using MVC and understanding the role of the model](https://stackoverflow.com/questions/54181162/php-structuring-a-slim3-web-application-using-mvc-and-understanding-the-role-o/54203726#54203726)