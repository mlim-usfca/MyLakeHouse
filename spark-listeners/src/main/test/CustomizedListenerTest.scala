import com.mylakehouse.CustomizedListener
import org.apache.spark.sql.SparkSession

object CustomizedListenerTest {
  def main(args: Array[String]): Unit = {
    // create a Spark session
    val sparkSession = SparkSession.builder()
      .master("local[*]")
      .config("spark.extraListeners", "com.mylakehouse.CustomizedListener") // ensures that the listener is instantiated before the Spark context is created
      .getOrCreate()

    // register the instantiated listener object with the Spark context
    val customizedListener_1 = new CustomizedListener
    sparkSession.sparkContext.addSparkListener(customizedListener_1)

    // create 1 application for Spark to do and for customized listener to log
    import sparkSession.implicits._
    (0 to 100).toDF("nr").repartition(30).collect()
  }
}
