import com.mylakehouse.CustomizedListener
import org.apache.spark.sql.SparkSession
import org.scalatest.funsuite.AnyFunSuite

class CustomizedListenerTest extends AnyFunSuite {
  // test whether the applicationSet is updated correctly
  test("applicationSet") {
    // Create a SparkSession
    val spark = SparkSession.builder()
      .appName("TestApp")
      .master("local[*]")
      .config("spark.extraListeners", "com.mylakehouse.CustomizedListener")
      .getOrCreate()
  }

  // test whether the queryMap is updated correctly
  test("queryMap") {
    // Create a SparkSession
    val spark = SparkSession.builder()
      .appName("TestApp")
      .master("local[*]")
      .config("spark.extraListeners", "com.mylakehouse.CustomizedListener")
      .getOrCreate()

    // Create a sample dataset
    val data = Seq(
      (1, "John", 25),
      (2, "Alice", 30),
      (3, "Bob", 35)
    )

    val df = spark.createDataFrame(data).toDF("id", "name", "age")
    df.createOrReplaceTempView("people")

    // Execute multiple SQL queries concurrently
    val query1 = spark.sql("SELECT * FROM people WHERE age > 30")
    val query2 = spark.sql("SELECT name, age FROM people")
    val query3 = spark.sql("SELECT COUNT(*) FROM people")

    // Collect the results
    val result1 = query1.collect()
    val result2 = query2.collect()
    val result3 = query3.collect()

    // Stop the Spark session
    spark.stop()
  }
}
