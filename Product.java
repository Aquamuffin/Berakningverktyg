
public class Product implements Comparable<Product> {
    String name;
    enum Material{
        Gjutjärn,
        Stål,
        RostfrittStål
    }
    Material mat;
    double[] Kvs;
    double[] D;
    double price;


    public Product(String name,double[] Kvs, double[] D, Material mat, double price){
        this.name = name;
        this.Kvs = Kvs;
        this.D = D;
        this.mat = mat;
        this.price = price;
    }

    public String getName(){
        return name;
    }

    public double[] getKvs(){
        return Kvs;
    }

    public double[] getD(){
        return D;
    }

    public Material getMaterial(){
        return mat;
    }

    public double getPrice(){
        return price;
    }

    public int compareTo(Product p){
        return (int) Math.round(price - p.getPrice());
    }

}
