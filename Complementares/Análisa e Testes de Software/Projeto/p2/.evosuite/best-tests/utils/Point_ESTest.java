/*
 * This file was automatically generated by EvoSuite
 * Fri Jan 17 14:27:32 GMT 2020
 */

package utils;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;
import utils.Point;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class Point_ESTest extends Point_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test0()  throws Throwable  {
      Double double0 = new Double(0.0);
      Point point0 = new Point(double0, double0);
      double double1 = point0.distanceBetweenPoints(point0);
      assertEquals(0.0, double1, 0.01);
  }

  @Test(timeout = 4000)
  public void test1()  throws Throwable  {
      Double double0 = new Double(943.67419);
      Point point0 = new Point(double0, double0);
      Double double1 = new Double((-2932.9948));
      Point point1 = new Point(double0, double1);
      double double2 = point0.distanceBetweenPoints(point1);
      assertEquals(3876.66899, double2, 0.01);
  }

  @Test(timeout = 4000)
  public void test2()  throws Throwable  {
      Double double0 = new Double(0.0);
      Point point0 = new Point(double0, double0);
      // Undeclared exception!
      try { 
        point0.distanceBetweenPoints((Point) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("utils.Point", e);
      }
  }

  @Test(timeout = 4000)
  public void test3()  throws Throwable  {
      Point point0 = null;
      try {
        point0 = new Point((Point) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("utils.Point", e);
      }
  }

  @Test(timeout = 4000)
  public void test4()  throws Throwable  {
      Point point0 = null;
      try {
        point0 = new Point((Double) null, (Double) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("utils.Point", e);
      }
  }

  @Test(timeout = 4000)
  public void test5()  throws Throwable  {
      Double double0 = new Double(10.764781015264882);
      Point point0 = new Point(double0, double0);
      String string0 = point0.toString();
      assertEquals("(10.76, 10.76)", string0);
  }

  @Test(timeout = 4000)
  public void test6()  throws Throwable  {
      Double double0 = new Double(10.764781015264882);
      Point point0 = new Point(double0, double0);
      Point point1 = new Point(point0);
      assertFalse(point1.equals((Object)point0));
  }
}
