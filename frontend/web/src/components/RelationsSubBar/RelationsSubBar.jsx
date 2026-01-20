import React, { useState } from "react";
import IndicatorButton from "../IndicatorButton/IndicatorButton";
import { SUBJECT_INDICATORS, OBJECT_INDICATORS } from "../../constants/relationsConfig";
import styles from "./RelationsSubBar.module.scss";

const RelationsSubBar = ({ onSelectionChange = () => {} }) => {
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [selectedObject, setSelectedObject] = useState(null);

  // Определяем доступность элементов левого столбца
  const getSubjectState = (subjectId) => {
    if (selectedSubject === subjectId) return 'selected';
    if (selectedObject) {
      const objectConfig = OBJECT_INDICATORS.find(o => o.id === selectedObject);
      if (objectConfig && !objectConfig.availableSubjects.includes(subjectId)) return 'disabled';
    }
    return 'default';
  };

  // Определяем доступность элементов правого столбца
  const getObjectState = (objectId) => {
    if (selectedObject === objectId) return 'selected';
    if (selectedSubject) {
      const subjectConfig = SUBJECT_INDICATORS.find(s => s.id === selectedSubject);
      if (subjectConfig && !subjectConfig.availableObjects.includes(objectId)) return 'disabled';
    }
    return 'default';
  };

  // Обработка кликов по субъектам
  const handleSubjectClick = (subjectId) => {
    const state = getSubjectState(subjectId);
    if (state === 'disabled') return;
    
    if (selectedSubject === subjectId) {
      // Deselect
      setSelectedSubject(null);
      onSelectionChange(null, selectedObject);
    } else {
      // Select new subject
      setSelectedSubject(subjectId);
      // Check if current object is still valid
      const subjectConfig = SUBJECT_INDICATORS.find(s => s.id === subjectId);
      if (selectedObject && subjectConfig && !subjectConfig.availableObjects.includes(selectedObject)) {
        setSelectedObject(null);
        onSelectionChange(subjectId, null);
      } else {
        onSelectionChange(subjectId, selectedObject);
      }
    }
  };

  // Обработка кликов по объектам
  const handleObjectClick = (objectId) => {
    const state = getObjectState(objectId);
    if (state === 'disabled') return;
    
    if (selectedObject === objectId) {
      // Deselect
      setSelectedObject(null);
      onSelectionChange(selectedSubject, null);
    } else {
      // Select new object
      setSelectedObject(objectId);
      // Check if current subject is still valid
      const objectConfig = OBJECT_INDICATORS.find(o => o.id === objectId);
      if (selectedSubject && objectConfig && !objectConfig.availableSubjects.includes(selectedSubject)) {
        setSelectedSubject(null);
        onSelectionChange(null, objectId);
      } else {
        onSelectionChange(selectedSubject, objectId);
      }
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.inner}>
        <div className={styles.column}>
          <h3 className={styles.columnTitle}>Показатель субъект</h3>
          <div className={styles.buttonList}>
            {SUBJECT_INDICATORS.map((subject) => (
              <IndicatorButton
                key={subject.id}
                label={subject.label}
                state={getSubjectState(subject.id)}
                onClick={() => handleSubjectClick(subject.id)}
                size="medium"
              />
            ))}
          </div>
        </div>

        <div className={styles.column}>
          <h3 className={styles.columnTitle}>Показатель объект</h3>
          <div className={styles.buttonList}>
            {OBJECT_INDICATORS.map((object) => (
              <IndicatorButton
                key={object.id}
                label={object.label}
                state={getObjectState(object.id)}
                onClick={() => handleObjectClick(object.id)}
                size="small"
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RelationsSubBar;
