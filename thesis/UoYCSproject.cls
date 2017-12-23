% Jeremy Jacob                                           UoYCSproject

% A class file to typeset BEng, Bsc, MEng, MMath and taught MSc
% project reports in the Department of Computer Science at the
% University of York.

% History
%
% Version 1
%
% 2004Apr27  Initial version
% 2004May10  Generation of list of tables and figures removed
% 2004Dec08  Minor fixes to error messages
% 2005Feb02  Package pdfcprot replaced by microtype 
% 2005Apr12  dedication and acknowledgements now come after abstract
% 2005Jul27  added option `sc' to `mathpazo' package & `textcomp' package
% 2005Aug31  added packages for Helvetica and Courier fonts
%
% Version 2 created, not backward compatible with Version 1
%
% 2006Mar23  moved front matter generation from \AtBeginDocument to
%            separately called \maketitle
% 2006Mar23  added options for choice of citation style
% 2006May12  improved communication with type area calculation
% 2006Jul03  added hypcap package
% 2006Dec10  added fixltx2e package
% 2007May31  fixed autoref names
% 2007Nov01  fixed Masters title names
% 2007Nov12  Added old-style text figures.
% 2008Oct03  used hyperref option `pdfusetitle'
% 2008Oct27  removed page numbers from `Part' pages
% 2009Jun26  changed to IEEE trans style; removed options.
% 2010Nov02  replaced obsolete KOMA-script options
% 2014Oct22  added ACS declaration
% 
% Version 3, backwards compatible
%
% 2015Apr24 Converted from BibTeX to BibLaTeX
% 2016Dec05 Brought up to date with latest Koma Script

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{UoYCSproject}[2016/12/05 Jeremy Jacob]

% Koma-script report style
\PassOptionsToPackage{twoside}{typearea}
\LoadClass[fontsize=11pt,a4paper,twoside,abstracton,numbers=noenddot,BCOR13mm]{scrreprt}
\RequirePackage{scrhack}

\RequirePackage[T1]{fontenc} % prevents < in text mode turning into
\RequirePackage{textcomp}    % ?', etc
\RequirePackage[osf]{mathpazo} % Palatino font
\RequirePackage{courier} % nicer typewriter-style fonts
\RequirePackage[scaled=.9]{helvet} % nice san serif fonts
\RequirePackage{microtype} % micro-typographical extensions for
                           % pdf(e)(la)tex
\RequirePackage[british]{babel} % British hyphenation patterns, etc.
\RequirePackage{ifthen}

\pagestyle{headings}
\renewcommand{\partpagestyle}{empty}

% Reference control
\RequirePackage{csquotes}

\typearea[current]{calc} % force page layout recalculation after
                         % changing all the fonts

\newcommand*{\UoYCSP@mk@degree}[1]{%
  \expandafter\def\csname#1\endcsname{\newcommand*{\UoYCSP@degree}{#1}}%
}
\UoYCSP@mk@degree{BEng}
\UoYCSP@mk@degree{BSc}
\UoYCSP@mk@degree{MEng}
\UoYCSP@mk@degree{MMath}
\newcommand*{\BScCS}{\newcommand*{\UoYCSP@degree}{BSc~in~Computer~Science}}
\newcommand*{\SWE}{\newcommand*{\UoYCSP@degree}{MSc~in~Software~Engineering}}
\newcommand*{\SCSE}{\newcommand*{\UoYCSP@degree}{MSc~in~Safety~Critical~Systems~Engineering}}
\newcommand*{\MIP}{\newcommand*{\UoYCSP@degree}{MSc~in~Information~Processing}}
\newcommand*{\MIT}{\newcommand*{\UoYCSP@degree}{MSc~in~Information~Technology}}
\newcommand*{\MNC}{\newcommand*{\UoYCSP@degree}{MSc~in~Natural~Computation}}
\newcommand*{\GTC}{\newcommand*{\UoYCSP@degree}{MSc~in~Gas~Turbine~Control}}
\newcommand*{\ACS}{\newcommand*{\UoYCSP@degree}{MSc~in~Advanced~Computer~Science}}

\newcommand*{\wordcount}[1]{\newcommand*{\UoYCSP@wordcount}{#1}}
\newcommand*{\includes}[1]{\renewcommand*{\UoYCSP@includes}{#1}}
\newcommand*{\UoYCSP@includes}{}
\newcommand*{\excludes}[1]{\renewcommand*{\UoYCSP@excludes}{#1}}
\newcommand*{\UoYCSP@excludes}{}
\newcommand*{\supervisor}[1]{\newcommand*{\UoYCSP@supervisor}{#1}}

\date{\fbox{\Huge DRAFT PROCESSED \today}}

\titlehead{The University of York\hfill Department of Computer Science}

\subject{%
  \ifx\UoYCSP@degree\undefined%
    \ClassError{UoYCSproject}%
               {degree scheme not set}
               {Declare the degree scheme in the preamble using
               \protect\BEng, \protect\MEng, etc.}
  \else%
    \large Submitted in part fulfilment for the degree of \break
    \UoYCSP@degree.%
  \fi%
}

\publishers{%
  \large

  \ifx\UoYCSP@supervisor\undefined%
    \ClassError{UoYCSproject}%
               {supervisor not set}
               {Declare the supervisor in the preamble using \protect\supervisor{Name}}  
  \else%
    Supervisor: \UoYCSP@supervisor%
  \fi%

  \vspace{\fill}

  \ifx\UoYCSP@wordcount\undefined%
    \ClassError{UoYCSproject}%
               {wordcount not set}
               {Declare the word count in the preamble using \protect\wordcount{Numeral}.} %
  \else
    Number of words = \UoYCSP@wordcount, as counted by
    \textsf{wc~-w}.
  \fi

  This includes the body of the report%
  \ifthenelse{    \equal{\UoYCSP@includes}{\@empty}
              \and\equal{\UoYCSP@excludes}{\@empty}}
             {\ only}
             {\ifthenelse{\equal{\UoYCSP@includes}{\@empty}}%
                         {}%
                         {, and \UoYCSP@includes}%
              \ifthenelse{\equal{\UoYCSP@excludes}{\@empty}}%
                         {}%
                         {, but not \UoYCSP@excludes}%
             }%
             .%
}

\let\old@abstract\abstract
\let\endold@abstract\endabstract
\renewcommand{\abstract}[1]{\newcommand{\UoYCSP@abstract}{#1}}
\renewcommand{\endabstract}{}

\let\old@dedication\dedication
\newcommand*{\UoYCSP@dedication}{}
\renewcommand*{\dedication}[1]{\renewcommand*{\UoYCSP@dedication}{#1}}
\newif\ifacknowledgements
\acknowledgementsfalse
\newcommand*{\UoYCSP@acknowledgements}{}
\newcommand{\acknowledgements}[1]{%
  \renewcommand{\UoYCSP@acknowledgements}{#1}%
  \acknowledgementstrue
}

\InputIfFileExists{\jobname.ldf}{}

\RequirePackage[pdfusetitle]{hyperref}% automatic hyperlinks, etc
\RequirePackage[all]{hypcap}% improve link placement in floats
\hypersetup{%
  pdfstartview={Fit}%
}
\urlstyle{sf}
\renewcommand*{\Itemautorefname}{Item}
\renewcommand*{\chapterautorefname}{Chapter}
\renewcommand*{\sectionautorefname}{Section}
\renewcommand*{\subsectionautorefname}{Subsection}
\renewcommand*{\subsubsectionautorefname}{Subsubsection}
\renewcommand*{\paragraphautorefname}{Paragraph}
\renewcommand*{\Hfootnoteautorefname}{Footnote}
%\renewcommand*{\pageautorefname}{Page}

\let\old@maketitle=\maketitle
\renewcommand*{\maketitle}{%
  \old@maketitle%
  \ifx\UoYCSP@abstract\undefined%
    \ClassError%
    {UoYCSproject}%
    {No abstract!}%
    {Declare an abstract in the preamble using \protect\abstract{Text}.}
  \else%
    \begin{old@abstract}%
      \UoYCSP@abstract%
    \end{old@abstract}%
  \fi%
  % dedication & acknowledgements
  \ifthenelse%
  {\equal{\UoYCSP@dedication}{\@empty}
         \and\equal{\UoYCSP@acknowledgements}{\@empty}}
  {}{
    \cleardoublepage%
    \thispagestyle{empty}
    \vspace*{\fill}%
    %
    \ifthenelse{\equal{\UoYCSP@dedication}{\@empty}}%
    {}%
    { \begin{center}%
        \large\UoYCSP@dedication%
      \end{center}%
    }%
    %
    \ifacknowledgements%
    { \vfill%
      \normalsize%
      \begin{center}%
        \large\bfseries Acknowledgements%
      \end{center}%
      \UoYCSP@acknowledgements%
    }%
    \fi%
    \vspace*{\fill}%
  }%
  \cleardoublepage%
  \microtypesetup{protrusion=false}%
  \tableofcontents%  
  \microtypesetup{protrusion=true}%
}

\AtBeginDocument{%
  \nonfrenchspacing%
}
