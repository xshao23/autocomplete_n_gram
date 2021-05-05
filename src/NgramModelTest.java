import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class NgramModelTest {


    @Test
    void testGetVocab() {
        NgramModel ng = new NgramModel(1,0);
        ng.update("abab");
        assertEquals(2,ng.getVocab().size());
        ng.update("abcd");
        assertEquals(4,ng.getVocab().size());
        
        NgramModel ng2 = new NgramModel(0,0);
        ng2.update("abab");
        assertEquals(2,ng2.getVocab().size());

    }

    @Test
    void testUpdateFile() {
        NgramModel ng = new NgramModel(8,0);
        ng.updateFile("pokemon.txt");
        assertEquals("zygarde",ng.getWord("~~~~~~zy"));
    }

    @Test
    void testProbability() {
        NgramModel ng = new NgramModel(1,0);
        ng.update("abab");
        ng.update("abcd");
        assertEquals(1,ng.probability("a", "b"),0.01);
        assertEquals(0,ng.probability("~", "c"),0.01);
        assertEquals(0.5,ng.probability("b", "c"),0.01);
    }
    

    @Test
    void testGetRandomChar() {
        NgramModel ng = new NgramModel(1,0);
        ng.update("abab");
        ng.update("abcd");
        assertEquals("b",ng.getRandomChar("a"));
        assertEquals("d",ng.getRandomChar("c"));
    }

    @Test
    void testGetWord() {
        NgramModel ng = new NgramModel(3,0);
        ng.update("abab");
        ng.update("rfgh");
        assertEquals("abab",ng.getWord("aba"));
    }

}
