import java.util.ArrayList;
import java.util.Scanner;

public class Driver{
    private static ArrayList<Dog> dogList = new ArrayList<Dog>();
    private static ArrayList<Monkey> monkeyList = new ArrayList<Monkey>();
    // Instance variables (if needed)
    
    
    // This method prints the menu options
    public static void displayMenu() {
        System.out.println("\n\n");
        System.out.println("\t\t\t\tRescue Animal System Menu");
        System.out.println("[1] Intake a new dog");
        System.out.println("[2] Intake a new monkey");
        System.out.println("[3] Reserve an animal");
        System.out.println("[4] Print a list of all dogs");
        System.out.println("[5] Print a list of all monkeys");
        System.out.println("[6] Print a list of all animals that are not reserved");
        System.out.println("[q] Quit application");
        System.out.println();
    }
      
    
    // Adds dogs to a list for testing
    public static void initializeDogList() {
        Dog dog1 = new Dog("Spot", "German Shepherd", "male", "1", "25.6", "05-12-2019", "United States", "intake", false, "United States");
        Dog dog2 = new Dog("Rex", "Great Dane", "male", "3", "35.2", "02-03-2020", "United States", "Phase I", false, "United States");
        Dog dog3 = new Dog("Bella", "Chihuahua", "female", "4", "25.6", "12-12-2019", "Canada", "in service", true, "Canada");
        
        dogList.add(dog1);
        dogList.add(dog2);
        dogList.add(dog3);
    }
    
    
    // Adds monkeys to a list for testing
    //Optional for testing
    public static void initializeMonkeyList() {
        Monkey monkey1 = new Monkey("Marcel", "Capuchin", "5.2", "9.4", "19.6", "male", "2", "15.3", "09-11-2019", "Canada", "Phase I", true, "Canada");
        Monkey monkey2 = new Monkey("Kong", "Macaque", "4.8", "10.2", "20.7", "female", "1", "17.4", "12-05-2020", "United Kingdom", "in service", false, "United Kingdom");
        Monkey monkey3 = new Monkey("Pat", "Tamarin", "5.5", "8.6", "18.4", "male", "3", "18.2", "12-10-2019", "United States", "intake", false, "United States");
        
        monkeyList.add(monkey1);
        monkeyList.add(monkey2);
        monkeyList.add(monkey3);
    }
    
    
    // Complete the intakeNewDog method
    // The input validation to check that the dog is not already in the list
    // is done for you
    public static void intakeNewDog(Scanner scanner) {
        System.out.println("What is the dog's name?");
        String name = scanner.nextLine();
        for(Dog dog: dogList) {
            if(dog.getName().equalsIgnoreCase(name)) {
                System.out.println("\n\nThis dog is already in our system\n\n");
                return; //returns to menu
            }
        }
    
    // Add the code to instantiate a new dog and add it to the appropriate list
        System.out.println("What is the dog's breed?");
        String breed = scanner.nextLine();
        System.out.println("What is the dog's gender?");
        String gender = scanner.nextLine();
        System.out.println("What is the dog's age?");
        String age = scanner.nextLine();
        System.out.println("What is the dog's weight?");
        String weight = scanner.nextLine();
        System.out.println("What is the dog's acquisition date?");
        String acqDate = scanner.nextLine();
        System.out.println("What is the dog's acquisition country?");
        String acqCountry = scanner.nextLine();
        System.out.println("What is the dog's training status?");
        String ts = scanner.nextLine();
        System.out.println("Is the dog reserved?");
        boolean res = scanner.nextBoolean();scanner.nextLine();
        System.out.println("What is the dog's in Service Country?");
        String isc = scanner.nextLine();
        Dog newdog=new Dog(name,breed,gender,age,weight,acqDate,acqCountry,ts,res,isc);
        dogList.add(newdog);
    }
    
    
    // Complete intakeNewMonkey
       //Instantiate and add the new monkey to the appropriate list
    // For the project submission you must also validate the input
       // to make sure the monkey doesn't already exist and the species type is allowed
    public static void intakeNewMonkey(Scanner scanner) {
        System.out.println("What is the monkey's name?");
        String name = scanner.nextLine();
        for(Monkey monkey: monkeyList) {
            if(monkey.getName().equalsIgnoreCase(name)) {
                System.out.println("\n\nThis monkey is already in our system\n\n");
                return; //returns to menu
            }
        }
        System.out.println("What is the monkey's species?");
        String species = scanner.nextLine();
        if(!(species.equalsIgnoreCase("Capuchin")) && !(species.equalsIgnoreCase("Guenon")) && !(species.equalsIgnoreCase("Macaque")) && !(species.equalsIgnoreCase("Marmoset")) && !(species.equalsIgnoreCase("Squirrel Monkey")) && !(species.equalsIgnoreCase("Tamarin"))){
            System.out.println("\n\nThis monkey's species is not allowed\n\n");
            return;
        }
        System.out.println("What is the monkey's tail length?");
        String tailLength = scanner.nextLine();
        System.out.println("What is the monkey's height?");
        String height = scanner.nextLine();
        System.out.println("What is the monkey's body length?");
        String bodyLength = scanner.nextLine();
        System.out.println("What is the monkey's gender?");
        String gender = scanner.nextLine();
        System.out.println("What is the monkey's age?");
        String age = scanner.nextLine();
        System.out.println("What is the monkey's weight?");
        String weight = scanner.nextLine();
        System.out.println("What is the monkey's acquisition date?");
        String acqDate = scanner.nextLine();
        System.out.println("What is the monkey's acquisition country?");
        String acqCountry = scanner.nextLine();
        System.out.println("What is the monkey's training status?");
        String ts = scanner.nextLine();
        System.out.println("Is the monkey reserved?");
        boolean res = scanner.nextBoolean();scanner.nextLine();
        System.out.println("What is the monkey's in Service Country?");
        String isc = scanner.nextLine();
        Monkey newmonkey=new Monkey(name,species,tailLength,height,bodyLength,gender,age,weight,acqDate,acqCountry,ts,res,isc);
        monkeyList.add(newmonkey);
    }
    
    // Complete reserveAnimal
    // You will need to find the animal by animal type and in service country
    public static void reserveAnimal(Scanner scanner) {
        System.out.println("The method reserveAnimal needs to be implemented");
    
    }
    
    // Complete printAnimals
    // Include the animal name, status, acquisition country and if the animal is reserved.
       // Remember that this method connects to three different menu items.
    // The printAnimals() method has three different outputs
    // based on the listType parameter
    // dog - prints the list of dogs
    // monkey - prints the list of monkeys
    // available - prints a combined list of all animals that are
    // fully trained ("in service") but not reserved
       // Remember that you only have to fully implement ONE of these lists.
       // The other lists can have a print statement saying "This option needs to be implemented".
       // To score "exemplary" you must correctly implement the "available" list.
    public static void printAnimals() {
        System.out.println("The method printAnimals needs to be implemented");
    
    }
    
    public static void main(String[] args) {
      
      
    
    
        initializeDogList();
        initializeMonkeyList();
        
        // Add a loop that displays the menu, accepts the users input
        // and takes the appropriate action.
           // For the project submission you must also include input validation
        // and appropriate feedback to the user.
        // Hint: create a Scanner and pass it to the necessary
        // methods
           // Hint: Menu options 4, 5, and 6 should all connect to the printAnimals() method.
        Scanner sc=new Scanner(System.in);
        displayMenu();
        System.out.println("Enter a menu selection");
        char input=sc.nextLine().charAt(0);
        if(input=='q'){
            System.exit(0);
        }
        int input1=Character.getNumericValue(input);
        while(input1<1 || input1>6){
            System.out.println("Invalid selection!");
            displayMenu();
            System.out.println("Enter a menu selection");
            input=sc.nextLine().charAt(0);            
            input1=Character.getNumericValue(input);
        }
        switch(input1){
            case 1:
                intakeNewDog(sc);
                break;
            case 2:
                intakeNewMonkey(sc);
                break;
            case 3:
                reserveAnimal(sc);
                break;
            case 4:
                printAnimals();
                break;
            case 5:
                printAnimals();
                break;
            case 6:
                System.exit(0);
        }        
    }
}
