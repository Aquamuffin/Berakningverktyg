import java.util.ArrayList;
import java.util.Iterator;
import java.util.Scanner;


//Computation tool for recommending products to customers based on their needs.

public class Berakningsverktyg {

	public static void main(String[] args){

        //Customer specifications

        Scanner scan = new Scanner(System.in);
        double p1 = scan.nextDouble();
        double p2 = scan.nextDouble();
        double Kv = scan.nextDouble();
        double Q = scan.nextDouble();
        String Medium = scan.next();
        
        Order.Medium M;
        switch (Medium) {
            case "vatten":
                M = Order.Medium.vatten;
                break;

            case "ånga":
                M = Order.Medium.ånga;
                break;
            case "gas":
                M = Order.Medium.gas;
                break;
            default:
                M = null;
                break;
        }
        Order in  = new Order(p1,p2,Kv,Q,M); 
        
        if(p2/p1 < 0.5){
            System.out.println("Cavitation warning, consult Ventim employee");
        }

        //Read list of available products from excel file

        ArrayList<Product> products = new ArrayList<Product>();

        

        //Loop through products to find the products that
        // fulfills criteria based on Kv, diameter, speed etc.
        ArrayList<Product> FittingProds = new ArrayList<Product>();
        for (Product product : products) {
            double[] Kvs = product.getKvs();
            double[] D = product.getD();
            for(int i = 0;i < Kvs.length;i++){
                if(Kvs[i] > in.getKv() && in.getV(D[i]) < 5){
                    FittingProds.add(product);
                    break;
                }
            }
        }

        FittingProds.sort(null);
        System.out.println(FittingProds.get(0));

    }


}
