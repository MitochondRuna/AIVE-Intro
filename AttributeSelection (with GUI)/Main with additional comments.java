/*
 *  Author: Eliza YU
 *  Additional comments added by Sean Chen
 *  Date: 4/23/2024
 *  Function: Attributes selection using Weka
 *  Version: 4-23 / 4.29 (fix save file function) / 4.30 (output logfile)
 *
 *  Improvements:
 *  1. Fixed the save file function (4.29/2024)
 *  2. Added logging functionality for processing results
 *  3. Automated the processing of ARFF files in a specified folder
 *
 *  Questions:
 *  1. What is the best way to select attributes?
 *  2. Which functions should be used?
 *  3. How to handle different ARFF files?
 */

package weka.api;

// Import necessary libraries
import java.io.File;
import java.io.IOException;
import java.util.logging.*;
import weka.attributeSelection.InfoGainAttributeEval;
import weka.attributeSelection.Ranker;
import weka.attributeSelection.AttributeSelection;
import weka.core.Instances;
import weka.core.converters.ArffSaver;
import weka.core.converters.ConverterUtils.DataSource;

/**
 * Main class for processing ARFF files to select attributes based on information gain.
 */
public class Main {
    // Logger for recording process information
    private static final Logger LOGGER = Logger.getLogger(Main.class.getName());

    /**
     * Sets up the logger to log messages to a file and console.
     *
     * @param outputDir the directory where log files will be saved
     */
    public static void setupLogger(File outputDir) {
        try {
            LogManager.getLogManager().reset(); // Reset default configuration
            LOGGER.setLevel(Level.ALL); // Set log level to all

            File logFile = new File(outputDir, "process_log.txt"); // Define log file
            FileHandler fileHandler = new FileHandler(logFile.getAbsolutePath(), true);
            fileHandler.setFormatter(new SimpleFormatter());
            LOGGER.addHandler(fileHandler);

            // Console output (optional)
            ConsoleHandler consoleHandler = new ConsoleHandler();
            consoleHandler.setLevel(Level.INFO);
            consoleHandler.setFormatter(new SimpleFormatter());
            LOGGER.addHandler(consoleHandler);
        } catch (IOException e) {
            LOGGER.log(Level.SEVERE, "Error setting up logger", e);
        }
    }

    /**
     * Processes all ARFF files in the specified input directory and saves the results to the output directory.
     *
     * @param inputDir  the directory containing input ARFF files
     * @param outputDir the directory where processed files will be saved
     */
    public static void processDirectory(File inputDir, File outputDir) {
        // Filter for ARFF files, excluding already processed ones
        File[] files = inputDir.listFiles((dir, name) -> name.toLowerCase().endsWith(".arff") && !name.toLowerCase().endsWith("_selection.arff"));

        if (files == null || files.length == 0) {
            LOGGER.info("No suitable ARFF files found in the directory.");
            return; // Early exit if no suitable files found
        }

        LOGGER.info("Total number of suitable ARFF files found: " + files.length); // Log number of files found

        for (int i = 0; i < files.length; i++) {
            LOGGER.info("Processing task " + (i + 1)); // Indicate the current task
            try {
                processFile(files[i], i + 1, outputDir); // Process each file
            } catch (Exception e) {
                LOGGER.log(Level.SEVERE, "Error processing file: " + files[i].getName(), e); // Log the error
            }
        }
        LOGGER.info("All tasks completed successfully."); // Indicate completion
    }

    /**
     * Processes a single ARFF file for attribute selection and saves the results.
     *
     * @param file       the ARFF file to process
     * @param taskNumber the task number for logging purposes
     * @param outputDir  the directory to save the output file
     * @throws Exception if an error occurs during processing
     */
    private static void processFile(File file, int taskNumber, File outputDir) throws Exception {
        // Load dataset from ARFF file
        DataSource source = new DataSource(file.getAbsolutePath());
        Instances dataset = source.getDataSet();

        // Set up attribute selection using information gain
        AttributeSelection filter = new AttributeSelection();
        InfoGainAttributeEval eval = new InfoGainAttributeEval();
        Ranker search = new Ranker();
        search.setThreshold(0.5); // Set threshold for attribute selection

        filter.setEvaluator(eval);
        filter.setSearch(search);

        // Apply attribute selection
        filter.SelectAttributes(dataset);
        Instances newData = filter.reduceDimensionality(dataset); // Reduce dimensionality

        // Prepare output file name and path
        String newFileName = getOutputFileName(file);
        String outputPath = new File(outputDir, newFileName).getAbsolutePath();

        // Save the new dataset
        ArffSaver saver = new ArffSaver();
        saver.setInstances(newData);
        saver.setFile(new File(outputPath));
        saver.writeBatch();

        // Log the processing results
        logFileProcessing(taskNumber, file.getName(), dataset.numAttributes(), newFileName, newData.numAttributes(), outputPath);
    }

    /**
     * Logs the processing results of a file.
     *
     * @param taskNumber       the task number for logging purposes
     * @param originalFileName the name of the original file
     * @param originalAttributes number of attributes in the original file
     * @param newFileName      the name of the new file created
     * @param newAttributes    number of attributes in the new file
     * @param outputPath       the path of the output file
     */
    private static void logFileProcessing(int taskNumber, String originalFileName, int originalAttributes, String newFileName, int newAttributes, String outputPath) {
        boolean saveSuccess = new File(outputPath).exists();
        LOGGER.info(String.format("Task %d // Input file: %s - attributes: %d // Output file: %s - attributes: %d - Save %s",
                taskNumber, originalFileName, originalAttributes, newFileName, newAttributes, saveSuccess ? "successful" : "failed"));
    }

    /**
     * Generates the output file name by appending "_selection" to the original file name.
     *
     * @param file the original ARFF file
     * @return the new file name
     */
    private static String getOutputFileName(File file) {
        String originalFileName = file.getName();
        String baseName = originalFileName.substring(0, originalFileName.lastIndexOf('.'));
        String extension = originalFileName.substring(originalFileName.lastIndexOf('.'));
        return baseName + "_selection" + extension; // Append "_selection" to the base name
    }

    /**
     * Main method to initiate processing of ARFF files.
     *
     * @param args command-line arguments (not used)
     */
    public static void main(String[] args) {
        // Specify the input and output directories
        File inputDir = new File("path_to_input_directory");
        File outputDir = new File("path_to_output_directory");
        setupLogger(outputDir); // Set up logging
        processDirectory(inputDir, outputDir); // Process the directory
    }
}
