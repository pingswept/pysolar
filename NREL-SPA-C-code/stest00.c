/*============================================================================
*
*    NAME:  stest00.c
*
*    PURPOSE:  Exercises the solar position algorithms in 'solpos.c'.
*
*        S_solpos
*            INPUTS:     year, daynum, hour, minute, second, latitude,
*                        longitude, timezone
*
*            OPTIONAL:   press   DEFAULT 1013.0 (standard pressure)
*                        temp    DEFAULT   10.0 (standard temperature)
*                        tilt    DEFAULT    0.0 (horizontal panel)
*                        aspect  DEFAULT  180.0 (South-facing panel)
*                        month   (if the S_DOY function is turned off)
*                        day     ( "             "             "     )
*
*            OUTPUTS:    amass, ampress, azim, cosinc, coszen, day, daynum,
*                        elevref, etr, etrn, etrtilt, month, prime,
*                        sbcf, sretr, ssetr, unprime, zenref
*
*       S_init        (optional initialization for all input parameters in
*                      the posdata struct)
*           INPUTS:     struct posdata*
*           OUTPUTS:    struct posdata*
*
*                     (Note: initializes the required S_solpos INPUTS above
*                      to out-of-bounds conditions, forcing the user to
*                      supply the parameters; initializes the OPTIONAL
*                      S_solpos inputs above to nominal values.)
*
*      S_decode       (optional utility for decoding the S_solpos return code)
*           INPUTS:     long int S_solpos return value, struct posdata*
*           OUTPUTS:    text to stderr
*
*
*        All variables are defined as members of the struct posdata
*        in 'solpos00.h'.
*
*    Usage:
*         In calling program, along with other 'includes', insert:
*
*              #include "solpos00.h"
*
*    Martin Rymes
*    National Renewable Energy Laboratory
*    25 March 1998
*
*    28 March 2001 REVISION:  SMW changed benchmark numbers to reflect the
*                             February 2001 changes to solpos00.c
*
*----------------------------------------------------------------------------*/
#include <math.h>
#include <string.h>
#include <stdio.h>

#include "solpos00.h"     /* <-- There is the 'include' I was talking about */

int main ( )
{
    struct posdata pd, *pdat; /* declare a posdata struct and a pointer for
                                 it (if desired, the structure could be
                                 allocated dynamically with malloc) */
    long retval;              /* to capture S_solpos return codes */


    /**************  Begin demo program **************/

    pdat = &pd; /* point to the structure for convenience */

    /* Initialize structure to default values. (Optional only if ALL input
       parameters are initialized in the calling code, which they are not
       in this example.) */

    S_init (pdat);

    /* I use Atlanta, GA for this example */

    pdat->longitude = -84.43;  /* Note that latitude and longitude are  */
    pdat->latitude  =  33.65;  /*   in DECIMAL DEGREES, not Deg/Min/Sec */
    pdat->timezone  =  -5.0;   /* Eastern time zone, even though longitude would
                                  suggest Central.  We use what they use.
                                  DO NOT ADJUST FOR DAYLIGHT SAVINGS TIME. */

    pdat->year      = 1999;    /* The year is 1999. */
    pdat->daynum    =  203;    /* July 22nd, the 203'rd day of the year (the
                                  algorithm will compensate for leap year, so
                                  you just count days). S_solpos can be
                                  configured to accept month-day dates; see
                                  examples below.) */

    /* The time of day (STANDARD time) is 9:45:37 */

    pdat->hour      =  9;
    pdat->minute    = 45;
    pdat->second    = 37;

    /* Let's assume that the temperature is 27 degrees C and that
       the pressure is 1006 millibars.  The temperature is used for the
       atmospheric refraction correction, and the pressure is used for the
       refraction correction and the pressure-corrected airmass. */

    pdat->temp      =   27.0;
    pdat->press     = 1006.0;

    /* Finally, we will assume that you have a flat surface facing southeast,
       tilted at latitude. */

    pdat->tilt      = pdat->latitude;  /* Tilted at latitude */
    pdat->aspect    = 135.0;       /* 135 deg. = SE */

    printf ( "\n" );
    printf ( "***** TEST S_solpos: *****\n" );
    printf ( "\n" );

    retval = S_solpos (pdat);  /* S_solpos function call */
    S_decode(retval, pdat);    /* ALWAYS look at the return code! */

    /* Now look at the results and compare with NREL benchmark */

    printf ( "Note that your final decimal place values may vary\n" );
    printf ( "based on your computer's floating-point storage and your\n" );
    printf ( "compiler's mathematical algorithms.  If you agree with\n" );
    printf ( "NREL's values for at least 5 significant digits, assume it works.\n\n" );

    printf ( "Note that S_solpos has returned the day and month for the\n");
    printf ( "input daynum.  When configured to do so, S_solpos will reverse\n");
    printf ( "this input/output relationship, accepting month and day as\n");
    printf ( "input and returning the day-of-year in the daynum variable.\n");
    printf ("\n" );
    printf ( "NREL    -> 1999.07.22, daynum 203, retval 0, amass 1.335752, ampress 1.326522\n" );
    printf ( "SOLTEST -> %d.%0.2d.%0.2d, daynum %d, retval %ld, amass %f, ampress %f\n",
      pdat->year, pdat->month, pdat->day, pdat->daynum,
      retval, pdat->amass, pdat->ampress );
    printf ( "NREL    -> azim 97.032875, cosinc 0.912569, elevref 48.409931\n" );
    printf ( "SOLTEST -> azim %f, cosinc %f, elevref %f\n",
      pdat->azim,    pdat->cosinc,    pdat->elevref );
    printf ( "NREL    -> etr 989.668518, etrn 1323.239868, etrtilt 1207.547363\n" );
    printf ( "SOLTEST -> etr %f, etrn %f, etrtilt %f\n",
      pdat->etr,    pdat->etrn,    pdat->etrtilt );
    printf ( "NREL    -> prime 1.037040, sbcf 1.201910, sunrise 347.173431\n" );
    printf ( "SOLTEST -> prime %f, sbcf %f, sunrise %f\n",
      pdat->prime,    pdat->sbcf,    pdat->sretr );
    printf ( "NREL    -> sunset 1181.111206, unprime 0.964283, zenref 41.590069\n" );
    printf ( "SOLTEST -> sunset %f, unprime %f, zenref %f\n",
      pdat->ssetr, pdat->unprime, pdat->zenref );



/**********************************************************************/
/* S_solpos configuration examples using the function parameter.

   Selecting a minimum of functions to meet your needs may result in
   faster execution.  A factor of two difference in execution speed
   exists between S_GEOM (the minimum configuration) and S_ALL (all
   variables calculated).  [S_DOY is actually the simplest and fastest
   configuration by far, but it only does the date conversions and bypasses
   all solar geometry.] If speed is not a consideration, use the default
   S_ALL configuration implemented by the call to S_init.

   The bitmasks are defined in S_solpos.h. */

    /* 1) Calculate the refraction corrected solar position variables */

    pdat->function = S_REFRAC;


    /* 2) Calculate the shadow band correction factor */

    pdat->function = S_SBCF;


    /* 3) Select both of the above functions (Note that the two bitmasks
          are 'or-ed' together to produce the desired results): */

    pdat->function = ( S_REFRAC | S_SBCF );


    /* 4) Modify the above configuration for accepting month and day rather
          than day-of-year.  Note that S_DOY (which controls on the day-of-year
          interpretation) must be inverted, then 'and-ed' with the other
          function codes to turn the day-of-year OFF.  With the day-of-year
	  bit off, S_solpos expects date input in the form of month and day. */

    pdat->function = ( (S_REFRAC | S_SBCF) & ~S_DOY );
    pdat->month = 7;
    pdat->day   = 22;

    /*    Also note that S_DOY is the only function that you should attempt
          to clear in this manner: Other function bitmasks are a composite
          of more than one mask, which represents an interdependency among
          functions. Turning off unexpected bits will produce unexpected
          results.  If in the course of your program you need fewer
          parameters calculated, you should rebuild the function mask
          from zero using only the required function bitmasks. */


    /* 5) Switch back to day-of-year in the above configuration by 'or-ing'
          with the bitmask */

    pdat->function |= S_DOY;
    pdat->month = -99;  /* Now ignore ridiculous month and day */
    pdat->day   = -99;  /* and overwrite them with correct values */

    /*    ... and back to month-day again, etc.: */

    pdat->function &= ~S_DOY;


    /* To see the effects of different configurations, move the above
       lines of code to just before the call to S_solpos and examine
       the results.  Note that some of the returned parameters are undefined
       if the configuration doesn't specify that they be calculated.  Thus,
       you must keep track of what you're calculating if you stray from the
       S_ALL default configuration. */


/**********************************************************************/
    /* Looking at the S_solpos return code

       In the return code, each bit represents an error in the range of
       individual input parameters.  See the bit definition in S_solpos.h
       for the position of each error flag.

       To assure that none of your input variables are out of bounds, the
       calling program should always look at the S_solpos return code.  In
       this example, the function S_decode fulfills that mandate by examining
       the code and writing an interpretation to the standard error output.

       To see the effect of an out of bounds parameter, move the following
       line to just before the call to S_solpos: */

    pdat->year = 99;  /* will S_solpos accept a two-digit year? */

    /* This causes S_decode to output a descriptive line regarding the value
       of the input year. [This algorithm is valid only between years 1950 and
       2050; hence, explicit four-digit years are required. If your dates are
       in a two-digit format, S_solpos requires that you make a conversion
       to an explicit four-digit year.]

       S_decode (located in the solpos.c file) can serve as a template for
       building your own decoder to handle errors according to the
       requirements of your calling application. */


/***********************************************************************/
    /* Accessing the individual functions */

    /* S_solpos was designed to calculate the output variables using the
       documented input variables.  However, as a matter of advanced
       programming convenience, the individual functions within S_solpos
       are accessible to the calling program through the use of the primative
       L_ masks (these are different from the composite S_ masks used
       above).  However, USE THESE WTTH CAUTION since the calling program
       must supply ALL parameters required by the function.  Because many of
       these variables are otherwise carefully created internally by
       S_solpos, the individual functions may not have bounds checking;
       hence your calling program must do all validation on the function
       input parameters. By the same reasoning, the return error code
       (retval) may not have considered all relevant input values, leaving
       the function vulnerable to computational errors or an abnormal end
       condition.

       As with the S_ masks above, the function variable is set to the
       L_ mask.  L_ masks may be ORed if desired.

       The solpos.h file contains a list of all output and transition
       variables, the reqired L_ mask, and all variables necessary for the
       calculation within individual functions.

       For example, the following code seeks only the amass value.  It calls
       only the airmass routine, which requires nothing but refracted zenith
       angle and pressure. Normally, the refracted zenith angle is a
       calculation that depends on many other functions within S_solpos.  But
       here using the L_ mask, we can simply set the refracted zenith angle
       externally and call the airmass function. */

    pdat->function = L_AMASS;  /* call only the airmass function */
    pdat->press    = 1013.0;   /* set your own pressure          */

    /* set up for the output of this example */
    printf( "Raw airmass loop:\n");
    printf( "NREL    -> 37.92  5.59  2.90  1.99  1.55  1.30  1.15  1.06  1.02  1.00\n");
    printf( "SOLTEST -> ");

    /* loop through a number of externally-set refracted zenith angles */
    for ( pdat->zenref = 90.0; pdat->zenref >= 0.0; pdat->zenref -= 10.0)
    {
      retval = S_solpos( pdat );        /* call solpos */
      S_decode( retval, pdat );         /* retval may not be valid */
      printf("%5.2f ", pdat->amass );   /* print out the airmass */
    }
    printf("\n");

    return 0;
}

