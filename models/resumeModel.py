from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl, Field
from datetime import date, datetime


class Location(BaseModel):
    address: Optional[str] = Field(None, description="To add multiple address lines, use \n. For example, 1234 Glücklichkeit Straße\nHinterhaus 5. Etage li.")
    postalCode: Optional[str] = None
    city: Optional[str] = None
    countryCode: Optional[str] = Field(None, description="code as per ISO-3166-1 ALPHA-2, e.g. US, AU, IN")
    region: Optional[str] = Field(None, description="The general region where you live. Can be a US state, or a province, for instance.")


class Profile(BaseModel):
    network: Optional[str] = Field(None, description="e.g. Facebook or Twitter")
    username: Optional[str] = Field(None, description="e.g. neutralthoughts")
    url: Optional[HttpUrl] = Field(None, description="e.g. http://twitter.example.com/neutralthoughts")


class Basics(BaseModel):
    name: Optional[str] = None
    label: Optional[str] = Field(None, description="e.g. Web Developer")
    image: Optional[str] = Field(None, description="URL (as per RFC 3986) to a image in JPEG or PNG format")
    email: Optional[EmailStr] = Field(None, description="e.g. thomas@gmail.com")
    phone: Optional[str] = Field(None, description="Phone numbers are stored as strings so use any format you like, e.g. 712-117-2923")
    url: Optional[HttpUrl] = Field(None, description="URL (as per RFC 3986) to your website, e.g. personal homepage")
    summary: Optional[str] = Field(None, description="Write a short 2-3 sentence biography about yourself")
    location: Optional[Location] = None
    profiles: Optional[List[Profile]] = Field(None, description="Specify any number of social networks that you participate in")


class WorkItem(BaseModel):
    name: Optional[str] = Field(None, description="e.g. Facebook")
    location: Optional[str] = Field(None, description="e.g. Menlo Park, CA")
    description: Optional[str] = Field(None, description="e.g. Social Media Company")
    position: Optional[str] = Field(None, description="e.g. Software Engineer")
    url: Optional[HttpUrl] = Field(None, description="e.g. http://facebook.example.com")
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    summary: Optional[str] = Field(None, description="Give an overview of your responsibilities at the company")
    highlights: Optional[List[str]] = Field(None, description="Specify multiple accomplishments")


class VolunteerItem(BaseModel):
    organization: Optional[str] = Field(None, description="e.g. Facebook")
    position: Optional[str] = Field(None, description="e.g. Software Engineer")
    url: Optional[HttpUrl] = Field(None, description="e.g. http://facebook.example.com")
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    summary: Optional[str] = Field(None, description="Give an overview of your responsibilities at the company")
    highlights: Optional[List[str]] = Field(None, description="Specify accomplishments and achievements")


class EducationItem(BaseModel):
    institution: Optional[str] = Field(None, description="e.g. Massachusetts Institute of Technology")
    url: Optional[HttpUrl] = Field(None, description="e.g. http://facebook.example.com")
    area: Optional[str] = Field(None, description="e.g. Arts")
    studyType: Optional[str] = Field(None, description="e.g. Bachelor")
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    score: Optional[str] = Field(None, description="grade point average, e.g. 3.67/4.0")
    courses: Optional[List[str]] = Field(None, description="List notable courses/subjects")


class AwardItem(BaseModel):
    title: Optional[str] = Field(None, description="e.g. One of the 100 greatest minds of the century")
    date: Optional[date] = None
    awarder: Optional[str] = Field(None, description="e.g. Time Magazine")
    summary: Optional[str] = Field(None, description="e.g. Received for my work with Quantum Physics")


class CertificateItem(BaseModel):
    name: Optional[str] = Field(None, description="e.g. Certified Kubernetes Administrator")
    issue_date: Optional[str] = Field(default=None, description="The date the certificate was issued, e.g., '2023-08-15'.")
    url: Optional[HttpUrl] = Field(None, description="e.g. http://example.com")
    issuer: Optional[str] = Field(None, description="e.g. CNCF")


class PublicationItem(BaseModel):
    name: Optional[str] = Field(None, description="e.g. The World Wide Web")
    publisher: Optional[str] = Field(None, description="e.g. IEEE, Computer Magazine")
    releaseDate: Optional[date] = None
    url: Optional[HttpUrl] = Field(None, description="e.g. http://www.computer.org.example.com/csdl/mags/co/1996/10/rx069-abs.html")
    summary: Optional[str] = Field(None, description="Short summary of publication. e.g. Discussion of the World Wide Web, HTTP, HTML.")


class SkillItem(BaseModel):
    name: Optional[str] = Field(None, description="e.g. Web Development")
    level: Optional[str] = Field(None, description="e.g. Master")
    keywords: Optional[List[str]] = Field(None, description="List some keywords pertaining to this skill")


class LanguageItem(BaseModel):
    language: Optional[str] = Field(None, description="e.g. English, Spanish")
    fluency: Optional[str] = Field(None, description="e.g. Fluent, Beginner")


class InterestItem(BaseModel):
    name: Optional[str] = Field(None, description="e.g. Philosophy")
    keywords: Optional[List[str]] = None


class ReferenceItem(BaseModel):
    name: Optional[str] = Field(None, description="e.g. Timothy Cook")
    reference: Optional[str] = Field(None, description="e.g. Joe blogs was a great employee, who turned up to work at least once a week. He exceeded my expectations when it came to doing nothing.")


class ProjectItem(BaseModel):
    name: Optional[str] = Field(None, description="e.g. The World Wide Web")
    description: Optional[str] = Field(None, description="Short summary of project. e.g. Collated works of 2017.")
    highlights: Optional[List[str]] = Field(None, description="Specify multiple features")
    keywords: Optional[List[str]] = Field(None, description="Specify special elements involved")
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    url: Optional[HttpUrl] = Field(None, description="e.g. http://www.computer.org/csdl/mags/co/1996/10/rx069-abs.html")
    roles: Optional[List[str]] = Field(None, description="Specify your role on this project or in company")
    entity: Optional[str] = Field(None, description="Specify the relevant company/entity affiliations e.g. 'greenpeace', 'corporationXYZ'")
    type: Optional[str] = Field(None, description=" e.g. 'volunteering', 'presentation', 'talk', 'application', 'conference'")


class Meta(BaseModel):
    canonical: Optional[HttpUrl] = Field(None, description="URL (as per RFC 3986) to latest version of this document")
    version: Optional[str] = Field(None, description="A version field which follows semver - e.g. v1.0.0")
    lastModified: Optional[datetime] = Field(None, description="Using ISO 8601 with YYYY-MM-DDThh:mm:ss")


class Resume(BaseModel):
    basics: Optional[Basics] = None
    work: Optional[List[WorkItem]] = None
    volunteer: Optional[List[VolunteerItem]] = None
    education: Optional[List[EducationItem]] = None
    awards: Optional[List[AwardItem]] = Field(None, description="Specify any awards you have received throughout your professional career")
    certificates: Optional[List[CertificateItem]] = Field(None, description="Specify any certificates you have received throughout your professional career")
    publications: Optional[List[PublicationItem]] = Field(None, description="Specify your publications through your career")
    skills: Optional[List[SkillItem]] = Field(None, description="List out your professional skill-set")
    languages: Optional[List[LanguageItem]] = Field(None, description="List any other languages you speak")
    interests: Optional[List[InterestItem]] = None
    references: Optional[List[ReferenceItem]] = Field(None, description="List references you have received")
    projects: Optional[List[ProjectItem]] = Field(None, description="Specify career projects")
    meta: Optional[Meta] = Field(None, description="The schema version and any other tooling configuration lives here")

