
//Class storing data to the computaion tool. 

public class Order {
    double p1;
    double p2;
    double Q;
    double Kv;
    enum Medium{
        vatten,
        ånga,
        gas
    }
    Medium med;
    // Constructor. Non-existing values are set to 0.
    public Order(double p1,double p2,double Q, double Kv,  Medium type){
    this.p1 = p1;
    this.p2 = p2;
    this.Q = Q;
    this.Kv = Kv;
    med = type;

    //Calculate potential missing values 
    if(med == Medium.vatten){
        if(Q == 0){
            Q = 1.25*Kv*Math.sqrt((p2-p1)/0.996);
        }
    
        if(Kv == 0){
            Kv = Q*Math.sqrt(0.996/(p2-p1));
        }
    }
    
    }

    public double getp1(){
        return p1;
    }

    public double getp2(){
        return p2;
    }

    public double getQ(){
        return Q;
    }

    public double getKv(){
        return Kv;
    }

    public double getV(double D){
        return 353*Q/(D*D);
    }

    public void getKv(double in){
        Kv = in;
    }

    public void getQ(double in){
        Q = in; 
    }

}
