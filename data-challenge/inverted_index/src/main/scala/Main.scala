import org.apache.spark.{SparkConf, SparkContext}

object Main extends App {
  // 1. Create Spark configuration
  val conf = new SparkConf()
    .setAppName("SparkMe Application")
    .setMaster("local[*]")  // local mode

  // 2. Create Spark context
  val sc = new SparkContext(conf)
  import sc.implicits._

  // Load the whole dataset as a Dataset it contains a Dataset[(String, String)] with (filename, content)
  val datasets = sc.wholeTextFiles("gs://castle-black-store/library/*").toDS()

  // Map the word separation function usign a regex, take the filename in the last position
  val dictionary = datasets.flatMap {
          case (path, content) =>
              content.split("""\W+""") map {
                  word => (word.toLowerCase, path.split("/").last)
              }
      }

  // groupByKey using the word and map the values as groups applying the sorting to the Int Iterator
  // The resulting object is still a Dataset[(String, Seq[Int])] with a sorted sequence.
  val xs = dictionary.groupByKey(_._1).mapValues(_._2.toInt).mapGroups( (key, iter) => (key, iter.to[SortedSet].toSeq))

  //Write the output to a single file
  xs.rdd.coalesce(1, shuffle = true).saveAsTextFile("gs://castle-black-store/output")
}
