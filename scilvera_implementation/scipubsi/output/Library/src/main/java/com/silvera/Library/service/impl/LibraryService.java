/**
    Use this file to implement business logic. This file will be preserved
    during next compilations.

    Generated by: silvera
    Date: 2022-05-22 03:03:00
*/

package com.silvera.Library.service.impl;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;

import com.silvera.Library.dto.PublishLogWithPaperDto;
import com.silvera.Library.service.dependencies.ScipaperClient;
import org.springframework.stereotype.Service;
import com.silvera.Library.domain.model.PublishLog;
import com.silvera.Library.service.base.*;
import com.silvera.Library.repository.*;
import com.silvera.Library.messages.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;


@Service
public class LibraryService implements ILibraryService {



    @Autowired
    ScipaperClient scipaperClient;

    

    @Autowired
    PublishLogRepository publishLogRepository;
    // Auto-generated CRUD methods





    
    @Override
    public java.util.List<PublishLogWithPaperDto> listPublishLogs(){

        var papers =scipaperClient.papers();
        var publishLogs = publishLogRepository.findAll();



        papers = papers.stream().filter(paper -> publishLogs.stream().anyMatch(publishLog -> Objects.equals(publishLog.getPaperId(), paper.getId()))).collect(Collectors.toList());

        var retVal = new ArrayList <PublishLogWithPaperDto>();

        for(var paper: papers){
            PublishLogWithPaperDto p = new PublishLogWithPaperDto();
            p.setPaper(paper);
            p.setPublishLog(publishLogs.stream().filter(publishLog -> Objects.equals(publishLog.getPaperId(), paper.getId())).findFirst().orElse(new PublishLog()));
            retVal.add(p);
        }

        return retVal;

    }

    
    @Override
    public void paperPublished(com.silvera.Library.messages.papermsggroup.PaperPublished message){
        PublishLog publishLog = new PublishLog();
        publishLog.setPaperId(Integer.valueOf(message.getPaperId()));
        publishLog.setAuthor(message.getAuthor());
        publishLog.setTitle(message.getTitle());

        publishLogRepository.save(publishLog);

    }
    
    

}