#pragma once
#ifndef MY_LumiMask_h
#define MY_LumiMask_h

#include <vector>
#include <string>
#include <algorithm>
#include <limits>
/**
 *  * Luminosity mask (constructed from a list of good lumi block ranges, as in the DQM JSON files)
 *   *
 *    * adopted from CMSSW code (EventSkipperByID and LuminosityBlockRange) for the minimal case needed here
 *     */
class LumiMask {
 public:
  using Run = unsigned int;
  using LumiBlock = unsigned int;

  /**
 *    * Luminosity block range - helper struct
 *       */
  class LumiBlockRange {
  public:
    LumiBlockRange(Run run, LumiBlock firstLumi, LumiBlock lastLumi)
      : m_run(run), m_firstLumi(firstLumi),
      m_lastLumi(lastLumi ? lastLumi : std::numeric_limits<LumiBlock>::max())
	{}
    Run run() const { return m_run; }
    LumiBlock firstLumi() const { return m_firstLumi; }
    LumiBlock lastLumi () const { return m_lastLumi ; }
    friend bool operator< ( const LumiMask::LumiBlockRange& lh, const LumiMask::LumiBlockRange& rh )
    {
      return ( lh.run() == rh.run() ) ? ( lh.lastLumi() < rh.firstLumi() ) : lh.run() < rh.run();
    }
  private:
    Run m_run;
    LumiBlock m_firstLumi;
    LumiBlock m_lastLumi;
  };

  explicit LumiMask(const std::vector<LumiBlockRange>& accept)
    : m_accept(accept)
  {
    std::sort(m_accept.begin(), m_accept.end());
  }

  bool accept(Run run, LumiBlock lumi) const
  { return std::binary_search(m_accept.begin(), m_accept.end(), LumiBlockRange(run, lumi, lumi)); }

  static LumiMask fromJSON(const std::string& fileName, LumiMask::Run firstRun=0, LumiMask::Run lastRun=0);

 private:
  std::vector<LumiBlockRange> m_accept;
};

#endif
