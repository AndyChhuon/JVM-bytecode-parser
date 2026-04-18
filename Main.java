import java.io.Serializable;
import java.util.List;

public final class Main implements Runnable, Serializable {
    private static final String test = "Hello world";
    private List<String> names;

    public static void main(String[] args){
        System.out.println(test);
    }


    @Override
    public void run() {
        System.out.println("running");
    }

    public String testAdd(String name) {
        names.add(name);
        return name;
    }
}