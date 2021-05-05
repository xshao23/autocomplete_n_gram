import java.util.*;

public class NgramRunner {

    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        System.out.println("Welcome to ngram, please enter the file you want to process");
        String filename = s.nextLine();
        int c = 6;
        NgramModel ng = new NgramModel(c,7);
        ng.updateFile(filename);;
        System.out.println("Please enter your input, if you want to quit please enter quit");
        
        String in = s.nextLine();
        while (!in.equals("quit")) {
            if (in.length()<c) {
                while (in.length()<c){
                    in = "~"+in;
                }
            }
            if (in.length()>c) {
               in  = in.substring(in.length()-c, in.length());
            }
            String ret = ng.getWord(in);
            if (ret.equals(in.replace("~", ""))) {
                System.out.println("Sorry no suggestions found");
            } else {
                System.out.println("Suggested word is: "+ret);
            }
            System.out.println("Please enter your input, if you want to quit please enter quit");
            in = s.nextLine();
        }

    }

}
