import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class NgramModel implements INgramModel {

    private int c; // c is the parameter in the Markov model, c = n - 1
    private int k; // parameter for smoothening the probability 
    private HashMap<String, TreeMap<String, Integer>> nGramsDict; 
                              // internal data structure for storing the context 
    private HashSet<String> vocab; // set that contains all vocabulary in the model
    
    public NgramModel(int c, int k) {
        this.c = c;
        this.k = k;
        this.vocab = new HashSet<>();
        this.nGramsDict = new HashMap<>();
    }
    
    @Override
    public HashSet<String> getVocab() {
        return this.vocab;
    }
    
    /**
     * This is a helper method that returns a padded string
     * @param n - number of "~" being padded 
     * @return a padded string 
     */
    private String startPad(int n) {
        String out = "";
        for (int i = 0; i < n; i++) {
            out += "~";
        }
        return out;
    }
    
    @Override
    public List<Tuple<String,String>> ngrams(int n, String text) {
        List<Tuple<String,String>> nGrams = new ArrayList<>();
        List<String> stack = new ArrayList<>();
        String pad = this.startPad(n);
        if (n == 0) {
            for (char ch:text.toCharArray()) {
                Tuple<String,String> t = new Tuple<String, String>("", "" + ch);
                nGrams.add(t);
            }
            return nGrams;
        }
        
        for (char ch:pad.toCharArray()) {
            stack.add("" + ch);
        }
        
        for (char ch: text.toCharArray()) {
            String tmp = "";
            for (String s : stack) {
                tmp += s;
            }
            Tuple<String,String> t = new Tuple<String, String>(tmp,ch + "");
            nGrams.add(t);
            stack.remove(0);
            stack.add(ch + ""); 
        }
        return nGrams;
    }

    @Override
    public void update(String text) {
        for (char ch: text.toCharArray()) {
            this.vocab.add(ch + "");
        }
        List<Tuple<String,String>> nGramsLi = this.ngrams(this.c, text);
        for (Tuple<String,String> t: nGramsLi) {
            String context = t.getLeft();
            String cha = t.getRight();
            TreeMap<String, Integer> charsInContext = 
                    this.nGramsDict.getOrDefault(context, new TreeMap<String, Integer>());
            int charFreqs = (int) charsInContext.getOrDefault(cha, 0);
            charFreqs += 1;
            charsInContext.put(cha,charFreqs);
            this.nGramsDict.put(context, charsInContext);             
        } 
    }
    
    @Override
    public void updateFile(String filename) {
        try {
            BufferedReader br = new BufferedReader(new FileReader(filename));
            try {
                if (br.ready()) {
                    //skip first line
                    br.readLine();
                    while (br.ready()) {
                        String[] currLine = br.readLine().trim().split("\\s+");
                        if (currLine.length == 2) {
                            String word = currLine[1].toLowerCase();
                            this.update(word);
                        }
                    }
                }
                br.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }
    
    @Override
    public double probability(String context, String character) {
        // TODO Auto-generated method stub
        if (nGramsDict.keySet().contains(context)) {
            TreeMap<String, Integer> charFreqsInContext = nGramsDict.get(context);
            int sum = 0; 
            for (int freq: charFreqsInContext.values()) {
                sum = sum + freq; 
            }
            int freq = charFreqsInContext.getOrDefault(character, 0);
            Double result = 1.0 * (freq + k) / (1.0 * (sum + k * vocab.size())); 
            return result; 
        } 
        return 1 / (1.0 * k * vocab.size());
    }

    @Override
    public String getChar(String context) {
        // return the most likely character
        if (nGramsDict.containsKey(context)) {
            TreeMap<String, Integer> charFreqsInContext = nGramsDict.get(context);
            String maxChar = ""; 
            Integer maxCount = 0; 
            for (String content: charFreqsInContext.keySet()) {
                if (maxCount < charFreqsInContext.get(content)) {
                    maxCount = charFreqsInContext.get(content); 
                    maxChar = content; 
                }
            }
            return maxChar; 
        } 
        int ind = new Random().nextInt(vocab.size());
        Object[] arr = vocab.toArray();
        return (String) arr[ind];
    }

    @Override
    public String getWord(String context) {
        String word = "";
        word += context;
        while (nGramsDict.containsKey(context)) {
            String newChar = getChar(context);  
            word += newChar; 
            context = word.substring(word.length() - c, word.length());
        }
        
        return word.replace("~", "");
    }

}


