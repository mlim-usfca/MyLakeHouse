package com.mylakehouse

import com.mylakehouse.CustomizedListener.getApplicationSet
import org.apache.spark.scheduler.{SparkListener, SparkListenerApplicationEnd, SparkListenerApplicationStart, SparkListenerEvent, SparkListenerTaskEnd, SparkListenerTaskStart}
import org.apache.spark.sql.execution.ui.{SparkListenerSQLExecutionEnd, SparkListenerSQLExecutionStart}
import org.apache.spark.sql.util.QueryExecutionListener
import org.apache.spark.sql.execution.QueryExecution

import scala.collection.mutable

// this object contains all static variables and methods that are shared among all instances of the com.mylakehouse.CustomizedListener class
object CustomizedListener {

  // create a mutable HashSet to store all IDs of applications that are currently running
  private val applicationSet = mutable.Set.empty[String]

  // create a mutable HashMap to store all IDs of queries that are currently running and the their associated application IDs
  private val queryMap = mutable.HashMap.empty[Long, String]

  // create a mutable HashMap to store all IDs of tasks that are currently running and the their associated application IDs
  private val taskMap = mutable.HashMap.empty[Long, String]

  // create a mutable HashMap to store the SQL context of a query (as the key)
  // and its application ID, duration/execution time, and error message if failed (as the value)
  private val sqlMap = mutable.HashMap.empty[String, (String, Long, String)]

  // create a method to return an immutable deep copy of applicationSet
  def getApplicationSet: Set[String] = applicationSet.toSet

  // create a method to return an immutable deep copy of queryMap
  def getQueryMap: Map[Long, String] = queryMap.toMap

  // create a method to return an immutable deep copy of taskMap
  def getTaskMap: Map[Long, String] = taskMap.toMap

  // create a method to return an immutable deep copy of sqlMap
  def getSQLMap: Map[String, (String, Long, String)] = sqlMap.toMap
}

class CustomizedListener extends SparkListener with QueryExecutionListener{
  private var curAppId = ""

  //  private var jvmGCTime = 0L
  //  private var totalRecordRead = 0L
  //  private var totalRecordWritten = 0L

  override def onApplicationStart(applicationStart: SparkListenerApplicationStart): Unit = {
    curAppId = applicationStart.appId.get
    CustomizedListener.applicationSet.add(curAppId)
    PushGateway.pushApplication(CustomizedListener.getApplicationSet)

    // print the HashSet after adding the ID of the application that has started
    println(s"Application started: ${getApplicationSet}")
  }

  override def onApplicationEnd(applicationEnd: SparkListenerApplicationEnd): Unit = {
    CustomizedListener.applicationSet.remove(curAppId)
    PushGateway.pushApplication(CustomizedListener.getApplicationSet)

    // print the HashSet after removing the ID of the application that has ended
    println(s"Application ended: ${getApplicationSet}")

    //    println(s"Total JVM GC time: ${jvmGCTime}")
    //    println(s"Total records read: ${totalRecordRead}")
    //    println(s"Total records written: ${totalRecordWritten}")
  }

  override def onTaskStart(taskStart: SparkListenerTaskStart): Unit = {
    val taskId = taskStart.taskInfo.taskId;
    val executorId = taskStart.taskInfo.executorId;
//    println(s"----------Task started: Task ID: ${taskId}, Executor ID: ${executorId}")
    CustomizedListener.taskMap.put(taskId, curAppId)
  }

  override def onTaskEnd(taskEnd: SparkListenerTaskEnd): Unit = {
    val taskId = taskEnd.taskInfo.taskId
//    println(s"----------Task ended: Task ID: $taskId")
    CustomizedListener.taskMap.remove(taskId)

    //    val metrics = taskEnd.taskMetrics
    //    val cpuTime = metrics.executorCpuTime
    //    jvmGCTime += metrics.jvmGCTime
    //    totalRecordRead += metrics.inputMetrics.recordsRead
    //    totalRecordWritten += metrics.outputMetrics.recordsWritten
    //    println(s"CPU Time: ${cpuTime}")
    //    println(s"JVM GC Time: ${jvmGCTime}")
    //    println(s"Total records read: ${totalRecordRead}")
    //    println(s"Total records written: ${totalRecordWritten}")
    //    println(s"Ended task with message: ${taskEnd}")
  }

  // override the onOtherEvent method to capture SQL-query events
  override def onOtherEvent(event: SparkListenerEvent): Unit = event match {
    case e: SparkListenerSQLExecutionStart => onSQLExecutionStart(e)
    case e: SparkListenerSQLExecutionEnd => onSQLExecutionEnd(e)
    case _ =>
  }

  // when a SQL query starts, create a method to capture its query Id and associate application Id
  // and add it to the queryMap which stores all currently running queries
  private def onSQLExecutionStart(event: SparkListenerSQLExecutionStart): Unit = {
    val queryId = event.executionId
    CustomizedListener.queryMap.put(queryId, curAppId)
    PushGateway.pushQuery(CustomizedListener.getQueryMap)
//    println(s"---------Query started: Query ID: $queryId, Application ID: $curAppId")

    // print all entries in HashMap after adding the query that has started
    //    println(s"HashMap after adding the query: ${CustomizedListener.getQueryMap}")
  }

  // when a SQL query ends, remove it from the queryMap
  private def onSQLExecutionEnd(event: SparkListenerSQLExecutionEnd): Unit = {
    val queryId = event.executionId
    CustomizedListener.queryMap.remove(queryId)
    PushGateway.pushQuery(CustomizedListener.getQueryMap)
//    println(s"----------Query ended: Query ID: $queryId")

    // print all entries in HashMap after removing the query that has ended
    //    println(s"HashMap after removing the query: ${CustomizedListener.getQueryMap}")
  }
  override def onSuccess(funcName: String, qe: QueryExecution, durationNs: Long): Unit = {
    println("=========================================")
    println("                 Print on success                 ")

    val sqlContext = qe.logical.origin.sqlText.getOrElse(qe.logical.toString())
    println(s"SQL query: $sqlContext")

    val sqlDuration = durationNs / 1000000
    println(s"Duration: $sqlDuration ms")

    // since the query has succeeded, there is no error message
    val errorMsg = "No error"
    println(s"Error message: $errorMsg")

    // put the sqlContext and its associated application ID, duration/execution time, and error message into the sqlMap
    CustomizedListener.sqlMap.put(sqlContext, (curAppId, sqlDuration, errorMsg))

//    PushGateway.pushQuery(CustomizedListener.getSQLMap)

    // remove the sqlContext from the sqlMap
    CustomizedListener.sqlMap.remove(sqlContext)

    println("=========================================")
  }

  override def onFailure(funcName: String, qe: QueryExecution, exception: Exception): Unit = {
    println("=========================================")
    println("                 Print on failure                 ")

    val sqlContext = qe.logical.origin.sqlText.getOrElse("Not a SQL query")
    println(s"SQL query: $sqlContext")

    // set the duration time to be 0 to indicate that the query has failed
    val sqlDuration = 0
    println(s"Duration: $sqlDuration ms")

    // since the query has failed, there is an error message
    val errorMsg = exception.getMessage
    println(s"Error message: $errorMsg")

    // put the sqlContext and its associated application ID, duration/execution time, and error message into the sqlMap
    CustomizedListener.sqlMap.put(sqlContext, (curAppId, sqlDuration, errorMsg))

    //    PushGateway.pushQuery(CustomizedListener.getSQLMap)

    // remove the sqlContext from the sqlMap
    CustomizedListener.sqlMap.remove(sqlContext)

    println("=========================================")
  }
}