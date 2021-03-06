/**
 * Scaffolding file used to store all the setups needed to run 
 * tests automatically generated by EvoSuite
 * Fri Jan 17 13:47:28 GMT 2020
 */

package controller;

import org.evosuite.runtime.annotation.EvoSuiteClassExclude;
import org.junit.BeforeClass;
import org.junit.Before;
import org.junit.After;
import org.junit.AfterClass;
import org.evosuite.runtime.sandbox.Sandbox;
import org.evosuite.runtime.sandbox.Sandbox.SandboxMode;

@EvoSuiteClassExclude
public class Controller_ESTest_scaffolding {

  @org.junit.Rule 
  public org.evosuite.runtime.vnet.NonFunctionalRequirementRule nfr = new org.evosuite.runtime.vnet.NonFunctionalRequirementRule();

  private static final java.util.Properties defaultProperties = (java.util.Properties) java.lang.System.getProperties().clone(); 

  private org.evosuite.runtime.thread.ThreadStopper threadStopper =  new org.evosuite.runtime.thread.ThreadStopper (org.evosuite.runtime.thread.KillSwitchHandler.getInstance(), 3000);


  @BeforeClass 
  public static void initEvoSuiteFramework() { 
    org.evosuite.runtime.RuntimeSettings.className = "controller.Controller"; 
    org.evosuite.runtime.GuiSupport.initialize(); 
    org.evosuite.runtime.RuntimeSettings.maxNumberOfThreads = 100; 
    org.evosuite.runtime.RuntimeSettings.maxNumberOfIterationsPerLoop = 10000; 
    org.evosuite.runtime.RuntimeSettings.mockSystemIn = true; 
    org.evosuite.runtime.RuntimeSettings.sandboxMode = org.evosuite.runtime.sandbox.Sandbox.SandboxMode.RECOMMENDED; 
    org.evosuite.runtime.sandbox.Sandbox.initializeSecurityManagerForSUT(); 
    org.evosuite.runtime.classhandling.JDKClassResetter.init();
    setSystemProperties();
    initializeClasses();
    org.evosuite.runtime.Runtime.getInstance().resetRuntime(); 
  } 

  @AfterClass 
  public static void clearEvoSuiteFramework(){ 
    Sandbox.resetDefaultSecurityManager(); 
    java.lang.System.setProperties((java.util.Properties) defaultProperties.clone()); 
  } 

  @Before 
  public void initTestCase(){ 
    threadStopper.storeCurrentThreads();
    threadStopper.startRecordingTime();
    org.evosuite.runtime.jvm.ShutdownHookHandler.getInstance().initHandler(); 
    org.evosuite.runtime.sandbox.Sandbox.goingToExecuteSUTCode(); 
    setSystemProperties(); 
    org.evosuite.runtime.GuiSupport.setHeadless(); 
    org.evosuite.runtime.Runtime.getInstance().resetRuntime(); 
    org.evosuite.runtime.agent.InstrumentingAgent.activate(); 
    org.evosuite.runtime.util.SystemInUtil.getInstance().initForTestCase(); 
  } 

  @After 
  public void doneWithTestCase(){ 
    threadStopper.killAndJoinClientThreads();
    org.evosuite.runtime.jvm.ShutdownHookHandler.getInstance().safeExecuteAddedHooks(); 
    org.evosuite.runtime.classhandling.JDKClassResetter.reset(); 
    resetClasses(); 
    org.evosuite.runtime.sandbox.Sandbox.doneWithExecutingSUTCode(); 
    org.evosuite.runtime.agent.InstrumentingAgent.deactivate(); 
    org.evosuite.runtime.GuiSupport.restoreHeadlessMode(); 
  } 

  public static void setSystemProperties() {
 
    java.lang.System.setProperties((java.util.Properties) defaultProperties.clone()); 
    java.lang.System.setProperty("file.encoding", "Cp1252"); 
    java.lang.System.setProperty("java.awt.headless", "true"); 
    java.lang.System.setProperty("java.io.tmpdir", "C:\\Users\\ASUS\\AppData\\Local\\Temp\\"); 
    java.lang.System.setProperty("user.country", "GB"); 
    java.lang.System.setProperty("user.dir", "C:\\Users\\ASUS\\Desktop\\MIEI\\4\u00BA Ano\\ATS\\ATS\\Projeto\\p2"); 
    java.lang.System.setProperty("user.home", "C:\\Users\\ASUS"); 
    java.lang.System.setProperty("user.language", "en"); 
    java.lang.System.setProperty("user.name", "ASUS"); 
    java.lang.System.setProperty("user.timezone", "Europe/London"); 
  }

  private static void initializeClasses() {
    org.evosuite.runtime.classhandling.ClassStateSupport.initializeClasses(Controller_ESTest_scaffolding.class.getClassLoader() ,
      "model.Client",
      "exceptions.InvalidCarException",
      "exceptions.InvalidUserException",
      "view.viewmodel.TimeInterval",
      "view.Menu$1",
      "model.Cars",
      "exceptions.InvalidNewRegisterException",
      "view.viewmodel.RentCarSimple",
      "view.viewmodel.AutonomyCar",
      "controller.Controller",
      "view.Menu",
      "exceptions.InvalidTimeIntervalException",
      "utils.Point",
      "view.viewmodel.CheapestNearCar",
      "model.Car$CarType",
      "view.viewmodel.NewLogin",
      "view.ITable",
      "exceptions.UnknownCompareTypeException",
      "utils.StringBetter",
      "model.Rental",
      "exceptions.UserExistsException",
      "model.User",
      "view.viewmodel.RegisterCar",
      "view.viewmodel.RateOwnerCar",
      "model.UMCarroJa",
      "exceptions.NoCarAvaliableException",
      "exceptions.InvalidNumberOfArgumentsException",
      "view.viewmodel.SpecificCar",
      "exceptions.UnknownCarTypeException",
      "exceptions.InvalidNewRentalException",
      "model.Users",
      "view.viewmodel.RegisterUser",
      "controller.Controller$1",
      "view.Table",
      "model.Owner",
      "model.Car",
      "exceptions.WrongPasswordExecption",
      "exceptions.CarExistsException",
      "model.Rentals",
      "exceptions.InvalidRatingException",
      "view.Menu$MenuInd"
    );
  } 

  private static void resetClasses() {
    org.evosuite.runtime.classhandling.ClassResetter.getInstance().setClassLoader(Controller_ESTest_scaffolding.class.getClassLoader()); 

    org.evosuite.runtime.classhandling.ClassStateSupport.resetClasses(
      "controller.Controller",
      "view.Menu$MenuInd",
      "controller.Controller$1",
      "model.UMCarroJa",
      "model.Cars",
      "model.Users",
      "model.Rentals",
      "utils.Point",
      "model.User",
      "model.Client",
      "exceptions.InvalidCarException",
      "exceptions.UnknownCompareTypeException",
      "model.Owner",
      "view.Menu",
      "view.Menu$1",
      "utils.StringBetter",
      "view.Table",
      "exceptions.InvalidUserException",
      "exceptions.NoCarAvaliableException",
      "model.Car",
      "view.viewmodel.RentCarSimple",
      "exceptions.InvalidTimeIntervalException",
      "exceptions.UserExistsException",
      "view.viewmodel.SpecificCar",
      "exceptions.InvalidNewRentalException",
      "view.viewmodel.NewLogin",
      "exceptions.WrongPasswordExecption"
    );
  }
}
