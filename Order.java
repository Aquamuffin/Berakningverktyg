//Klass som lagrar indata till beräkningsverktyget. 

public class Order {
    double p1;
    double p2;
    double Q;
    double Kv;
    double D;

    public Order(double p1,double p2,double Q, double Kv, double D){
    this.p1 = p1;
    this.p2 = p2;
    this.Q = Q;
    this.Kv = Kv;
    this.D = D;
    }

    public double Getp1(){
        return p1;
    }

    public double Getp2(){
        return p2;
    }

    public double GetQ(){
        return Q;
    }

    public double GetKv(){
        return Kv;
    }

    public double GetD(){
        return D;
    }

    public void SetKv(double in){
        Kv = in;
    }

    public void SetQ(double in){
        Q = in; 
    }

}
