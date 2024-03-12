package listeners

import org.apache.spark.scheduler.{SparkListener, SparkListenerApplicationEnd, SparkListenerApplicationStart,
  SparkListenerStageCompleted, SparkListenerTaskEnd, SparkListenerTaskStart}
import org.apache.spark.sql.SparkSession

object SparkListener {

  def main(args: Array[String]): Unit = {
    val sparkSession = SparkSession.builder().master("local[*]").getOrCreate()
    sparkSession.sparkContext.addSparkListener(LogPrintingListener)

    // create some Spark tasks for the listener to log
    import sparkSession.implicits._
    (0 to 100).toDF("nr").repartition(30).collect()
  }
}

object LogPrintingListener extends SparkListener {
  private var jvmGCTime = 0L
  private var totalRecordRead = 0L
  private var totalRecordWritten = 0L
  private var stageMap = Map[Int, Int]()

  override def onApplicationStart(applicationStart: SparkListenerApplicationStart): Unit = {
    val appId = applicationStart.appId
    val userId = applicationStart.sparkUser
    println(s"Application ID: ${appId.getOrElse("None")}, user ID: $userId")
  }

  override def onApplicationEnd(applicationEnd: SparkListenerApplicationEnd): Unit = {
    println(s"Total JVM GC time: ${jvmGCTime}")
    println(s"Total records read: ${totalRecordRead}")
    println(s"Total records written: ${totalRecordWritten}")
    println(s"Stages: ${stageMap}")
  }

  override def onTaskStart(taskStart: SparkListenerTaskStart): Unit = {
    val taskId = taskStart.taskInfo.taskId;
    val executorId = taskStart.taskInfo.executorId;
    println(s"Started task with the message: ${taskStart}")
    println(s"Task ID: ${taskId}, Executor ID: ${executorId}")
  }

  override def onTaskEnd(taskEnd: SparkListenerTaskEnd): Unit = {
    val metrics = taskEnd.taskMetrics

    val cpuTime = metrics.executorCpuTime;
    jvmGCTime += metrics.jvmGCTime
    totalRecordRead += metrics.inputMetrics.recordsRead
    totalRecordWritten += metrics.outputMetrics.recordsWritten
    println(s"CPU Time: ${cpuTime}")
    println(s"JVM GC Time: ${jvmGCTime}")
    println(s"Total records read: ${totalRecordRead}")
    println(s"Total records written: ${totalRecordWritten}")
    println(s"Ended task with message: ${taskEnd}")
  }

  override def onStageCompleted(stageCompleted: SparkListenerStageCompleted): Unit = {
    val tasks = stageCompleted.stageInfo.numTasks
    val stageId = stageCompleted.stageInfo.stageId
    stageMap += (stageId -> tasks)
    println(s"Stage ID: ${stageId}, Tasks: ${tasks}")
  }

}