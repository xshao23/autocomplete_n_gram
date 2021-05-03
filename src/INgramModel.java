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
    public HashSet getVocab();
    
    /**
     * update the N-gram model with words in the training data 
     * @param text - a word in the training data
     */
    public void update(String text);
    
    /**
     * Given a context string, calculate the 
     * @param context - a string represents of the context that precedes the predicted character 
     * @param character - a character that we want to predict the probability on 
     * @return the probability that the character may entails given the input context
     */
    public double probability(String context, String character); 
    
    /**
     * Generate a random character based on the context 
     * @param context - a string represents of the context that precedes the predicted character 
     * @return a char that entails the context
     */
    public String getRandomChar(String context); 
    
    /**
     * Complete the word given the context
     * @param context - a string represents of the context that precedes the predicted character 
     * @return word predicted 
     */
    public String getWord(String context); 
    
}
