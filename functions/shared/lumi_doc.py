# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from enum import StrEnum
from dataclasses import dataclass
from shared.types import ArxivMetadata, LoadingStatus
from typing import List, Optional


@dataclass
class Position:
    start_index: int
    end_index: int


@dataclass
class Highlight:
    color: str
    span_id: str
    position: Position


@dataclass
class Citation:
    span_id: str
    position: Position


@dataclass
class CitedContent:
    text: str
    citations: List[Citation]


@dataclass
class Label:
    id: str
    label: str


@dataclass
class LumiSummary:
    id: str
    summary: "LumiSpan"


@dataclass
class LumiSummaries:
    section_summaries: List[LumiSummary]
    content_summaries: List[LumiSummary]
    span_summaries: List[LumiSummary]
    abstract_excerpt_span_id: str | None = None


@dataclass
class Heading:
    heading_level: int
    text: str


@dataclass
class ConceptContent:
    label: str
    value: str


@dataclass
class LumiConcept:
    id: str
    name: str
    contents: List[ConceptContent]
    in_text_citations: List[Label]


@dataclass
class LumiSection:
    id: str
    heading: Heading
    contents: List["LumiContent"]
    sub_sections: Optional[List["LumiSection"]] = None


@dataclass
class TextContent:
    tag_name: str
    spans: List["LumiSpan"]


@dataclass
class ImageContent:
    storage_path: str
    latex_path: str
    alt_text: str
    width: float
    height: float
    caption: Optional["LumiSpan"] = None


@dataclass
class FigureContent:
    images: List[ImageContent]
    caption: Optional["LumiSpan"] = None


@dataclass
class HtmlFigureContent:
    html: str
    caption: Optional["LumiSpan"] = None


@dataclass
class ListContent:
    list_items: List["ListItem"]
    is_ordered: bool


@dataclass
class ListItem:
    spans: List["LumiSpan"]
    subListContent: ListContent | None = None


@dataclass
class LumiContent:
    id: str
    text_content: Optional[TextContent] = None
    image_content: Optional[ImageContent] = None
    figure_content: Optional[FigureContent] = None
    html_figure_content: Optional[HtmlFigureContent] = None
    list_content: Optional[ListContent] = None


@dataclass
class LumiSpan:
    id: str
    text: str
    inner_tags: List["InnerTag"]


class InnerTagName(StrEnum):
    BOLD = "b"
    ITALIC = "i"
    STRONG = "strong"
    EM = "em"
    UNDERLINE = "u"
    MATH = "math"
    MATH_DISPLAY = "math_display"
    REFERENCE = "ref"
    SPAN_REFERENCE = "spanref"
    CONCEPT = "concept"
    A = "a"
    CODE = "code"
    FOOTNOTE = "footnote"


@dataclass
class InnerTag:
    id: str
    tag_name: InnerTagName
    metadata: dict
    position: "Position"
    # These are additional recursive tags within the content of this inner tag.
    # This may happen if we have e.g. <b>[lumi-start-concept]...[lumi-end-concept]</b>
    children: List["InnerTag"]


@dataclass
class LumiReference:
    id: str
    span: LumiSpan


@dataclass
class LumiFootnote:
    id: str
    span: LumiSpan


@dataclass
class LumiAbstract:
    contents: List[LumiContent]


@dataclass
class LumiDoc:
    """Class for LumiDoc, a preprocessed Lumi document representation of a paper."""

    markdown: str

    sections: List[LumiSection]
    concepts: List[LumiConcept]
    abstract: Optional[LumiAbstract] = None
    references: Optional[List[LumiReference]] = None
    footnotes: Optional[List[LumiFootnote]] = None
    summaries: Optional[LumiSummaries] = None
    metadata: Optional[ArxivMetadata] = None
    loading_status: Optional[LoadingStatus] = LoadingStatus.UNSET
    loading_error: Optional[str] = None
