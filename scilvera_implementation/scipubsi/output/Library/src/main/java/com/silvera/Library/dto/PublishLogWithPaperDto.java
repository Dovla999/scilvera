package com.silvera.Library.dto;

import com.silvera.Library.domain.model.PublishLog;
import com.silvera.Library.domain.model.dependencies.Paper;

public class PublishLogWithPaperDto {
    private Paper paper;

    public Paper getPaper() {
        return paper;
    }

    public void setPaper(Paper paper) {
        this.paper = paper;
    }
    private PublishLog publishLog;

    public PublishLog getPublishLog() {
        return publishLog;
    }

    public void setPublishLog(PublishLog publishLog) {
        this.publishLog = publishLog;
    }
}
