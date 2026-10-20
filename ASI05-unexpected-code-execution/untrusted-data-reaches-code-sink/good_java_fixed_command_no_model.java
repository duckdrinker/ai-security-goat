package demo;

public class ShellHelper {
    public void listFiles() throws Exception {
        Runtime.getRuntime().exec(new String[] {"ls", "-l"});
    }
}