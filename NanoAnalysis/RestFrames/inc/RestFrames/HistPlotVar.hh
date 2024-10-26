/////////////////////////////////////////////////////////////////////////
//   RestFrames: particle physics event analysis library
//   --------------------------------------------------------------------
//   Copyright (c) 2014-2016, Christopher Rogan
/////////////////////////////////////////////////////////////////////////
///
///  \file   HistPlotVar.hh
///
///  \author Christopher Rogan
///          (crogan@cern.ch)
///
///  \date   2015 Jul
///
//   This file is part of RestFrames.
//
//   RestFrames is free software; you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation; either version 2 of the License, or
//   (at your option) any later version.
// 
//   RestFrames is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU General Public License for more details.
// 
//   You should have received a copy of the GNU General Public License
//   along with RestFrames. If not, see <http://www.gnu.org/licenses/>.
/////////////////////////////////////////////////////////////////////////

#ifndef HistPlotVar_HH
#define HistPlotVar_HH

#include "RestFrames/RFBase.hh"

namespace RestFrames {

  ///////////////////////////////////////////////
  // HistPlotVar class
  ///////////////////////////////////////////////
  class HistPlotVar : public RFBase {

  public:
    HistPlotVar(const std::string& name, 
		const std::string& title, 
		double minval, double maxval,
		const std::string& unit);
    HistPlotVar();
    ~HistPlotVar();

    void operator = (double val) const;

    void operator += (double val) const;

    void operator -= (double val) const;

    void operator *= (double val) const;

    void operator /= (double val) const;

    operator double() const;

    double GetVal() const;

    double GetMin() const;

    double GetMax() const;

    std::string GetUnit() const;

    static HistPlotVar& Empty();

  private:
    /// \brief HistPlotCategory ID key
    static int m_class_key;

    std::string m_Unit;
    double m_Min;
    double m_Max;
    mutable double m_Val;

    static HistPlotVar m_Empty;

  };

}

#endif
