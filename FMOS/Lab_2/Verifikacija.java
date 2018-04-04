import gov.nasa.jpf.vm.Verify;
import javax.annotation.Nonnull;
import gov.nasa.jpf.annotation.Const;

/**
 *
 * @author Korisnik
 */
public class Verifikacija {
   @Nonnull private String id;
   @Const private String DNA;
   
  Verifikacija (String s){
    id = s.toUpperCase();
    DNA  = "AGTC";
  }
    
  public static void main (String[] args){
    double vel = Verify.getDouble("velocity");
   
    assert (vel < 100.0);
    
    Verifikacija v = new Verifikacija("a");
    v.setId(null);
    v.setDNA("CTGA");
  }
  public void setId(String id){
      this.id = id;
  }
  public void setDNA(String DNA){
      this.DNA = DNA;
  }
}