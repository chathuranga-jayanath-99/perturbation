public class Calculator {

    public static void main(String[] args) {
        // Example usage
        int a = 10;
        int b = 5;

        int sum = add(a, b);
        int difference = subtract(a, b);

        System.out.println("Sum: " + sum);
        System.out.println("Difference: " + difference);
    }

    // Function to add two numbers
    public static int add(int num1, int num2) {
        return num1 + num2;
    }

    // Function to subtract two numbers
    public static int subtract(int num1, int num2) {
        return num1 - num2;
    }
}
