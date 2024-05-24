/*
 *  author： Eliza YU
 *  data : 4/23/2024
 *  function: attributes selection
 *  version: 4-23/ 4.29(fix save file function)/ 4.30 (output logfile)
 *
 *  improvement (all finished):
 *  1. fix the save file function (fixed in  4.29/2024)
 *      [already fixed, the only thing to change is to add the VM option in "config",
 *      command line:--add-opens=java.base/java.lang=ALL-UNNAMED]
 *  2. output a log file, including file-formal attr and number - new file attr and number - success or not[finished]
 *  3. write a script to automate process files in a folder, and output to XXX folder.
 *
 *  Question: what is the best way to select attributes? which functions? what if use different arrf files?
 *
 */

package weka.api;



// file path and dir
import java.io.File;
import java.io.IOException;
import java.util.logging.*;
import java.io.FilenameFilter;
// process attributes
import weka.attributeSelection.CfsSubsetEval;
import weka.attributeSelection.GreedyStepwise;
import weka.core.Instances;
import weka.filters.Filter;
import weka.filters.supervised.attribute.AttributeSelection;
import weka.core.converters.ArffSaver;
import weka.core.converters.ConverterUtils.DataSource;

public class Main {
    // choose a folder full of arff file
//    public static void main(String[] args) {
//        File directory = new File("C:/Users/鱼畅/AIVE/MembranePrediction/WEKA file merge/Example weka data files/Dataset 1 CoreA files");
//        // Avoid process the arff file generate
//        File[] files = directory.listFiles((dir, name) -> name.toLowerCase().endsWith(".arff") && !name.toLowerCase().endsWith("_selection.arff"));
//
//        if (files == null || files.length == 0) {
//            System.out.println("No suitable ARFF files found in the directory.");
//            return;  // Early exit if no suitable files found
//        }
//
//        System.out.println("Total number of suitable ARFF files found: " + files.length);  // Print the number of suitable files found
//
//        for (int i = 0; i < files.length; i++) {
//            System.out.println("Processing task " + (i + 1) );  // Indicate the current task
//            try {
//                processFile(files[i], i + 1);
//            } catch (Exception e) {
//                System.err.println("Error processing file: " + files[i].getName());
//                e.printStackTrace();  // Print the stack trace if there's an error
//            }
//        }
//        System.out.println("All tasks completed successfully.");  // Indicate completion
//    }

    // set up log file
    private static final Logger LOGGER = Logger.getLogger(Main.class.getName());

    public static void setupLogger(File outputDir) {
        try {
            LogManager.getLogManager().reset(); // 重置以清除默认配置
            LOGGER.setLevel(Level.ALL); // 设置日志级别

            File logFile = new File(outputDir, "process_log.txt"); // 定义日志文件
            FileHandler fileHandler = new FileHandler(logFile.getAbsolutePath(), true);
            fileHandler.setFormatter(new SimpleFormatter());
            fileHandler.setLevel(Level.INFO);
            LOGGER.addHandler(fileHandler);

            // 控制台输出，可选
            ConsoleHandler consoleHandler = new ConsoleHandler();
            consoleHandler.setLevel(Level.INFO);
            consoleHandler.setFormatter(new SimpleFormatter());
            LOGGER.addHandler(consoleHandler);
        } catch (IOException e) {
            LOGGER.log(Level.SEVERE, "Error setting up logger", e);
        }
    }

    //
    public static void processDirectory(File inputDir, File outputDir) {

        File[] files = inputDir.listFiles((dir, name) -> name.toLowerCase().endsWith(".arff") && !name.toLowerCase().endsWith("_selection.arff"));

        if (files == null || files.length == 0) {
            LOGGER.info("No suitable ARFF files found in the directory.");
            return;  // Early exit if no suitable files found
        }

        LOGGER.info("Total number of suitable ARFF files found: " + files.length);  // Print the number of suitable files found

        for (int i = 0; i < files.length; i++) {
            LOGGER.info("Processing task " + (i + 1));  // Indicate the current task
            try {
                processFile(files[i], i + 1, outputDir);
            } catch (Exception e) {
                LOGGER.info("Error processing file: " + files[i].getName());
                e.printStackTrace();  // Print the stack trace if there's an error
            }
        }
        LOGGER.info("All tasks completed successfully.");  // Indicate completion
    }

    private static void processFile(File file, int taskNumber, File outputDir) throws Exception {
        DataSource source = new DataSource(file.getAbsolutePath());
        Instances dataset = source.getDataSet();

        AttributeSelection filter = new AttributeSelection();
        CfsSubsetEval eval = new CfsSubsetEval();
        GreedyStepwise search = new GreedyStepwise();
        search.setSearchBackwards(true);
        filter.setEvaluator(eval);
        filter.setSearch(search);
        filter.setInputFormat(dataset);
        Instances newData = Filter.useFilter(dataset, filter);

        String originalFileName = file.getName();
        String baseName = originalFileName.substring(0, originalFileName.lastIndexOf('.'));
        String extension = originalFileName.substring(originalFileName.lastIndexOf('.'));
        String newFileName = baseName + "_selection" + extension;
        String outputPath = outputDir.getAbsolutePath() + File.separator + newFileName; // 使用指定的输出目录

        ArffSaver saver = new ArffSaver();
        saver.setInstances(newData);
        saver.setFile(new File(outputPath));
        saver.writeBatch();

        File outputFile = new File(outputPath);
        boolean saveSuccess = outputFile.exists();

        LOGGER.info(String.format("Task %d // Input file: %s - attributes: %d // Output file: %s - attributes: %d - Save %s",
                taskNumber, originalFileName, dataset.numAttributes(), newFileName, newData.numAttributes(), saveSuccess ? "successful" : "failed"));
    }

    public static void main(String[] args) {
        // 仅用于测试或直接调用
        File inputDir = new File("path_to_input_directory");
        File outputDir = new File("path_to_output_directory");
        processDirectory(inputDir, outputDir);
    }
}
