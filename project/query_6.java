//STEP 1. Import required packages
import java.sql.Connection;
import java.sql.Driver;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import org.apache.commons.math3.stat.correlation.PearsonsCorrelation;

public class Query6 {
   // JDBC driver name and database URL
   static final String JDBC_DRIVER = "oracle.jdbc.driver.OracleDriver";  
   static final String DB_URL = "jdbc:oracle:thin:@//dbod-scan.acsu.buffalo.edu:1521/cse00000.buffalo.edu";

   //  Database credential
   static final String USER = "mvenkata";
   static final String PASS = "cse601";
   
   public static void main(String[] args) throws SQLException {
   Connection conn = null;
   Statement stmt = null;
   try{
      //STEP 2: Register JDBC driver
      Class.forName("oracle.jdbc.driver.OracleDriver");

      //STEP 3: Open a connection
      System.out.println("Connecting to database...");
      conn = DriverManager.getConnection(DB_URL,USER,PASS);

      //STEP 4: Execute a query
      System.out.println("Creating statement...");
      stmt = conn.createStatement();
      String sql;
       
      sql = "SELECT COUNT(MF.EXP) FROM CLINICAL_FACT CF INNER JOIN " +"	MICROARRAY_FACT MF ON CF.S_ID=MF.S_ID WHERE CF.S_ID IN ( " +
		"SELECT DISTINCT S_ID FROM CLINICAL_FACT WHERE P_ID IN (" +
   		"SELECT P_ID FROM CLINICAL_FACT WHERE DS_ID IN (SELECT DS_ID FROM DISEASE" +
   		" WHERE NAME='ALL')) AND S_ID IS NOT NULL )" +
"AND MF.PB_ID IN " +
	"(SELECT MF.PB_ID FROM MICROARRAY_FACT MF INNER JOIN PROBE PB ON MF.PB_ID=PB.PB_ID WHERE PB.PB_ID IN " +
		"(SELECT PB.PB_ID FROM PROBE PB INNER JOIN GENE_FACT GF ON PB.U_ID=GF.GENE_UID WHERE GF.GENE_UID IN" +
			"(SELECT GF.GENE_UID FROM GENE_FACT GF WHERE GO_ID=0007154)))";
      
      
      ResultSet rs = stmt.executeQuery(sql);
      //STEP 5: Extract data from result set
      ArrayList<Double> list1 = new ArrayList<Double>();
      ArrayList<Double> list2 = new ArrayList<Double>();
      
      double sample1Sum = 0.0;
      
      while(rs.next()){
         Double exp = rs.getDouble("EXP");
         sample1Sum += exp
         list1.add(exp);
      }
      int count1=list1.size();
      double mean1 = sample1Sum/count1;
      double[] sample1 = new double[count1];
     	
      for(int i = 0; i < count1; i++) {
    	  sample1[i] = list1.get(i);
    	  variance1 += Math.pow(sample1[i] - mean1, 2); 
      }
     variance1 = variance1 / (count1 - 1);     
      
      //Similarly get the next sample
      
      sql = "SELECT COUNT(MF.EXP) FROM CLINICAL_FACT CF INNER JOIN MICROARRAY_FACT MF ON CF.S_ID=MF.S_ID WHERE CF.S_ID IN ( " +
	 "SELECT DISTINCT S_ID FROM CLINICAL_FACT WHERE P_ID IN ( " +
   		"SELECT P_ID FROM CLINICAL_FACT WHERE DS_ID IN (SELECT DS_ID FROM DISEASE WHERE NAME='AML')) AND S_ID IS NOT NULL) " + 
"AND MF.PB_ID IN " +
	"(SELECT MF.PB_ID FROM MICROARRAY_FACT MF INNER JOIN PROBE PB ON MF.PB_ID=PB.PB_ID WHERE PB.PB_ID IN " +
		"(SELECT PB.PB_ID FROM PROBE PB INNER JOIN GENE_FACT GF ON PB.U_ID=GF.GENE_UID WHERE GF.GENE_UID IN " +
			"(SELECT GF.GENE_UID FROM GENE_FACT GF WHERE GO_ID=0007154)))";

      
 
      
      rs = stmt.executeQuery(sql);
      //STEP 5: Extract data from result set
      double sample2Sum=0;
      
      while(rs.next()){
         double exp = rs.getDouble("EXP");
         list2.add(exp);
         //System.out.println(" EXP: " + exp);
      }
      double[] sample2 = new double[list2.size()];
      // double variance2 = 0;
      int i = 0;
      for(; i < count2; i++) {
    	  sample2[i] = list2.get(i);
    	  variance2 += Math.pow( sample2[i] - mean2, 2);
      }
      
      System.out.println("-----List 1---------");
      System.out.println(list1);
      
      System.out.println("-------List 2-------");
      System.out.println(list2);
      
      PearsonsCorrelation p = new PearsonsCorrelation();
      double cor = 0.0;
      int count = 0
      for(int i = 0; i < col.size() - 1; i++) {
      	for(int j = i + 1; j < col.size(); j++) {
      		System.out.println(i + ":" + j);
      		count++;
      		cor += p.correlation(col.get(i), col.get(j)); 
      	}
      }
      
      double avgCor = cor/count;
      
      System.out.println("result for ALL to ALL is ");
      System.out.println(avgCor);

      //ALL to AML
      double cor2 = 0.0;
      for(int i = 0; i < allList.size(); i++) {
      	for(int j = 0; j < amlList.size(); j++) {
      		cor2 += p.correlation(allList.get(i), amlList.get(j)); 
      	}
      }
      double avgCor2 = cor2 /(allList.size() * amlList.size()) ;

      System.out.println("result for ALL to AML is ");
      System.out.println(avgCor2);
      //STEP 6: Clean-up environment
      rs.close();
      stmt.close();
      conn.close();
   }catch(SQLException se){
      se.printStackTrace();
   }catch(Exception e){
      e.printStackTrace();
   }finally{
      try{
         if(stmt!=null)
            stmt.close();
      }catch(SQLException se2){
      }
      try{
         if(conn!=null)
            conn.close();
      }catch(SQLException se){
         se.printStackTrace();
      }
   }
   System.out.println("Goodbye!");
   }
}
