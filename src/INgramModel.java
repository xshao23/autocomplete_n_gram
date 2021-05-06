import java.util.*;
/**
 * 
 * @author Xuchong Shao, Xinyi Li 
 *
 */
public interface INgramModel {
    
    
    /**
     * Return the vocabulary learned by the N-gram model 
     * @return a set of of vocabulary 
     */
    public HashSet<String> getVocab();
    
    /**
     * The method convert a string to list of tuples of n-grams
     * each tuple contains a context and a character token
     * @param n - parameter of n-gram
     * @param text - string being converted to n-grams 
     * @return a list of tuples 
     */
    public List<Tuple<String,String>> ngrams(int n, String text);
    
    
    /**
     * update the N-gram model with words in the training data 
     * @param text - a word in the training data
     */
    public void update(String text);
    
    /**
     * This method takes in a path of the file that contains the dictionary 
     * and updates internal map with words learned  
     * @param file - file path 
     */
    public void updateFile(String file);
    
    /**
     * Given a context string, calculate the 
     * @param context - a string represents of the context that precedes the predicted character 
     * @param character - a character that we want to predict the probability on 
     * @return the probability that the character may entails given the input context
     */
    public double probability(String context, String character); 
    
    /**
     * Generate the most likely character based on the context 
     * @param context - a string represents of the context that precedes the predicted character 
     * @return a char that entails the context
     */
    public String getChar(String context); 
    
    /**
     * Complete the word given the context
     * @param context - a string represents of the context that precedes the predicted character 
     * @return word predicted 
     */
    public String getWord(String context); 
    
}
