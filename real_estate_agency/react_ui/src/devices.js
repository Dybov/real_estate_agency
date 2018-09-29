// Extra small
const XS = 0;
// Small
const SM = 768;
// Medium
const MD = 992;
// Large
const LG = 1200;

/**
 * Check if device's innerWidth lower than medium (MD)
 *
 * @return {bool} is device lower than MD.
 */
function ltMD() {return window.innerWidth < MD}
/**
 * Check if device's innerWidth lower than large (LG)
 *
 * @return {bool} is device lower than MD.
 */
function ltLG() {return window.innerWidth < LG}
/**
 * Check if device's innerWidth greater than extra small (XS)
 *
 * @return {bool} is device lower than MD.
 */
function gtXS() {return SM <= window.innerWidth }
/**
 * Check if device's innerWidth greater than medium (MD)
 *
 * @since      0.0.1
 *
 * @return {bool} is device lower than MD.
 */
function gtSM() {return MD <= window.innerWidth }


module.exports = {
  XS:XS,
  SM:SM,
  MD:MD,
  LG:LG,

  isXS: () => {return window.innerWidth < SM},
  isSM: () => {return (SM <= window.innerWidth) && (window.innerWidth < MD)},
  isMD: () => {return (MD <= window.innerWidth) && (window.innerWidth < LG)},
  isLG: () => {return LG <= window.innerWidth},

  ltMD: ltMD,
  ltLG: ltLG,

  lteSM: () => {return ltMD()},
  lteMD: () => {return ltLG()},

  gtXS: gtXS,
  gtSM: gtSM,

  gteSM: () => {return gtXS()},
  gteMD: () => {return gtSM()},

}