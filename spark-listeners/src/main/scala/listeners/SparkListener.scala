package listeners

import org.apache.spark.scheduler.{SparkListener, SparkListenerApplicationEnd, SparkListenerApplicationStart,
                                   SparkListenerStageCompleted, SparkListenerTaskEnd, SparkListenerTaskStart}
import org.apache.spark.sql.SparkSession

object SparkListener {

  def main(args: Array[String]): Unit = {
    val sparkSession = SparkSession.builder().master("local[*]").getOrCreate()
    sparkSession.sparkContext.addSparkListener(LogPrintingListener)
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
    // TODO: discuss with the team to see
    //       if the project requires what info when application starts
  }

  override def onApplicationEnd(applicationEnd: SparkListenerApplicationEnd): Unit = {
    // TODO: discuss with the team to see
    //       if the project requires what info when application ends
  }

  override def onTaskStart(taskStart: SparkListenerTaskStart): Unit = {
    val taskId = taskStart.taskInfo.taskId;
    val executorId = taskStart.taskInfo.executorId;
    // TODO: discuss with the team to see
    //       if the project requires what info when a task starts
  }

  override def onTaskEnd(taskEnd: SparkListenerTaskEnd): Unit = {
    val metrics = taskEnd.taskMetrics

    val cpuTime = metrics.executorCpuTime;
    jvmGCTime += metrics.jvmGCTime
    totalRecordRead += metrics.inputMetrics.recordsRead
    totalRecordWritten += metrics.outputMetrics.recordsWritten
    // TODO: discuss with the team to see
    //       if the project requires what info when a task ends
  }

  override def onStageCompleted(stageCompleted: SparkListenerStageCompleted): Unit = {
    val tasks = stageCompleted.stageInfo.numTasks
    val stageId = stageCompleted.stageInfo.stageId
    stageMap += (stageId -> tasks)
    // TODO: discuss with the team to see
    //       if the project requires what info when a stage ends
  }

  // TODO: discuss with the team to see if the project requires any other info
}