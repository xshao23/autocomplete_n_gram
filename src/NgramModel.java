import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class NgramModel implements INgramModel{

    private int c;
    private int k;
    private HashMap<String, TreeMap<String, Integer>> nGramsDict;
    private HashSet<String> vocab;
    
    public NgramModel(int c, int k){
        this.c=c;
        this.k=k;
        this.vocab= new HashSet<>();
        this.nGramsDict=new HashMap<>();
    }
    
    @Override
    public HashSet getVocab() {
        return this.vocab;
    }
    
    private String start_pad(int n) {
        String out = "";
        for (int i = 0; i < n; i++){
            out+="~";
         }
        return out;
    }
    
    @Override
    public List<Tuple<String,String>> ngrams(int n, String text) {
        List<Tuple<String,String>> n_grams = new ArrayList<>();
        List<String> stack = new ArrayList<>();
        String pad = this.start_pad(n);
        if (n==0) {
            for (char ch:text.toCharArray()) {
                Tuple<String,String> t = new Tuple<String, String>("", ""+ch);
                n_grams.add(t);
            }
            return n_grams;
        }
        
        for (char ch:pad.toCharArray()) {
            stack.add(""+ch);
        }
        
        for (char ch: text.toCharArray()) {
            String tmp = "";
            for (String s : stack){
                tmp+=s;
            }
            Tuple<String,String> t = new Tuple<String, String>(tmp,ch+"");
            n_grams.add(t);
            stack.remove(0);
            stack.add(ch+""); 
        }
        return n_grams;
    }

    @Override
    public void update(String text) {
        for (char ch: text.toCharArray()) {
            this.vocab.add(ch+"");
        }
        List<Tuple<String,String>> n_grams_li = this.ngrams(this.c, text);
        for (Tuple<String,String> t: n_grams_li) {
            String context = t.getLeft();
            String cha = t.getRight();
            TreeMap chars_in_context = (TreeMap) this.nGramsDict.getOrDefault(context, new TreeMap());
            int char_freqs = (int) chars_in_context.getOrDefault(cha, 0);
            char_freqs+=1;
            chars_in_context.put(cha,char_freqs);
            this.nGramsDict.put(context, chars_in_context);             
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
                        //read each line and add them into the trie
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
            Double result = 1.0 * (freq + k)/ (1.0 * (sum + k * vocab.size())); 
            return result; 
        } 
        return 1 / (1.0 * k * vocab.size());
    }

    @Override
    public String getRandomChar(String context) {
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
        word+=context;
        while (nGramsDict.containsKey(context)) {
            String newChar = getRandomChar(context);  
            word+=newChar; 
            context = word.substring(word.length()-c, word.length());
        }
        
        return word.replace("~", "");
    }

}


